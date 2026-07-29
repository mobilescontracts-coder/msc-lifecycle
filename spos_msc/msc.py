"""Mobile smart-contract lifecycle functions for SPoS-MSC."""

from __future__ import annotations

import hashlib
import random
from collections import defaultdict

from .config import PrototypeConfig
from .models import (
    CommitteeMember,
    EvidenceEvent,
    FinalityCertificate,
    MobileTransaction,
    Receipt,
    RewardEvent,
    RoutedTransaction,
)
from .spos import committee_is_viable, select_finality_participants


def edge_package(tx: MobileTransaction) -> EvidenceEvent:
    return EvidenceEvent(event_type="edge_packaged_request", value=tx.tx_id, tx_id=tx.tx_id)


def route_transactions(
    transactions: list[MobileTransaction],
    initial_load: dict[int, float],
    config: PrototypeConfig,
) -> tuple[list[RoutedTransaction], dict[int, float], list[EvidenceEvent]]:
    """Route transactions with simple load-aware shard choice.

    Cross-shard transactions prefer their source shard but may be moved when a shard
    exceeds the load threshold. This is intentionally simple and readable.
    """
    routed: list[RoutedTransaction] = []
    evidence: list[EvidenceEvent] = []
    load = dict(initial_load)
    for shard in range(1, config.shard_count + 1):
        load.setdefault(shard, 0.0)

    for tx in transactions:
        preferred = 1 + (tx.contract_id % config.shard_count)
        if load[preferred] >= config.rebalance_threshold:
            target = min(load, key=load.get)
            reason = "rebalance_lowest_load"
        else:
            target = preferred
            reason = "contract_mapping"
        routed.append(RoutedTransaction(shard_id=target, tx=tx, route_reason=reason))
        # Payload and cross-shard dependency increase load.
        load[target] += 0.25 + tx.payload_size * 0.05 + (0.3 if tx.cross_shard else 0.0)
        evidence.append(EvidenceEvent("routed_tx", target, tx_id=tx.tx_id, shard_id=target))
    return routed, load, evidence


def run_finality(
    routed: list[RoutedTransaction],
    committees: dict[int, list[CommitteeMember]],
    rng: random.Random,
    config: PrototypeConfig,
    connectivity_penalty: float = 0.0,
) -> tuple[list[FinalityCertificate], list[EvidenceEvent]]:
    certs: list[FinalityCertificate] = []
    evidence: list[EvidenceEvent] = []
    for item in routed:
        committee = committees.get(item.shard_id, [])
        if not committee_is_viable(committee, config):
            evidence.append(EvidenceEvent("finality_failed_underfilled_committee", 1, item.tx.tx_id, item.shard_id))
            continue
        base_failure = 0.01
        cross_penalty = 0.04 if item.tx.cross_shard else 0.0
        failure_prob = base_failure + cross_penalty + connectivity_penalty
        if rng.random() < failure_prob:
            evidence.append(EvidenceEvent("finality_failed_probabilistic", 1, item.tx.tx_id, item.shard_id))
            continue
        proposer, voters = select_finality_participants(committee, rng)
        h = hashlib.sha256(f"{item.shard_id}|{item.tx.tx_id}|{proposer}|{voters}".encode()).hexdigest()[:16]
        latency = (
            config.edge_latency
            + config.block_time
            + config.finality_latency
            + (6 if item.tx.cross_shard else 0)
            + rng.uniform(-2.0, 2.0)
            + connectivity_penalty * 35
        )
        certs.append(
            FinalityCertificate(
                tx_id=item.tx.tx_id,
                shard_id=item.shard_id,
                proposer_id=proposer,
                voter_ids=voters,
                certificate_hash=h,
                finality_time=max(latency, 1.0),
            )
        )
        evidence.append(EvidenceEvent("finality_certificate", 1, item.tx.tx_id, item.shard_id))
    return certs, evidence


def generate_receipts_rewards(
    certs: list[FinalityCertificate],
    rng: random.Random,
    config: PrototypeConfig,
    receipt_penalty: float = 0.0,
) -> tuple[list[Receipt], list[RewardEvent], list[EvidenceEvent]]:
    receipts: list[Receipt] = []
    rewards: list[RewardEvent] = []
    evidence: list[EvidenceEvent] = []
    for cert in certs:
        if rng.random() < receipt_penalty:
            evidence.append(EvidenceEvent("receipt_failed", 1, cert.tx_id, cert.shard_id))
            continue
        receipt_time = cert.finality_time + config.receipt_latency + rng.uniform(0, 3)
        receipts.append(Receipt(cert.tx_id, cert.shard_id, "FINAL", max(receipt_time, cert.finality_time)))
        evidence.append(EvidenceEvent("mobile_receipt", 1, cert.tx_id, cert.shard_id))

        rewards.append(
            RewardEvent(
                validator_id=cert.proposer_id,
                reward=config.reward_finality + config.reward_receipt + config.proposer_bonus,
                reason="proposer_finality_receipt",
                tx_id=cert.tx_id,
                shard_id=cert.shard_id,
            )
        )
        for voter in cert.voter_ids:
            rewards.append(
                RewardEvent(
                    validator_id=voter,
                    reward=config.voter_reward,
                    reason="voter_finality",
                    tx_id=cert.tx_id,
                    shard_id=cert.shard_id,
                )
            )
    return receipts, rewards, evidence


def shard_load_std(load: dict[int, float]) -> float:
    values = list(load.values())
    if not values:
        return 0.0
    mean_load = sum(values) / len(values)
    return (sum((v - mean_load) ** 2 for v in values) / len(values)) ** 0.5


def reconfiguration_events(load: dict[int, float], config: PrototypeConfig) -> int:
    return sum(1 for value in load.values() if value >= config.rebalance_threshold)
