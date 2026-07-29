"""Typed data models used by the SPoS-MSC prototype."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Validator:
    vid: int
    owner_id: int
    stake: int
    mobile_fitness: int
    attack_risk: int
    availability: int = 100


@dataclass(frozen=True)
class ValidatorScore:
    vid: int
    owner_id: int
    raw_stake: int
    owner_total_stake: int
    owner_adjusted_stake: float
    mobile_fitness: int
    attack_risk: int
    score: float
    eligible: bool
    reason: str = "eligible"


@dataclass(frozen=True)
class MobileTransaction:
    tx_id: int
    sender: str
    contract_id: int
    payload_size: int
    cross_shard: bool = False
    source_shard: int | None = None
    target_shard: int | None = None


@dataclass(frozen=True)
class CommitteeMember:
    shard_id: int
    validator_id: int
    role: str
    selection_hash: int


@dataclass(frozen=True)
class RoutedTransaction:
    shard_id: int
    tx: MobileTransaction
    route_reason: str


@dataclass(frozen=True)
class FinalityCertificate:
    tx_id: int
    shard_id: int
    proposer_id: int
    voter_ids: tuple[int, ...]
    certificate_hash: str
    finality_time: float


@dataclass(frozen=True)
class Receipt:
    tx_id: int
    shard_id: int
    status: str
    receipt_time: float


@dataclass(frozen=True)
class RewardEvent:
    validator_id: int
    reward: int
    reason: str
    tx_id: int
    shard_id: int


@dataclass(frozen=True)
class EvidenceEvent:
    event_type: str
    value: Any
    tx_id: int | None = None
    shard_id: int | None = None


@dataclass(frozen=True)
class ScenarioConfig:
    scenario_id: str
    name: str
    tx_count_range: tuple[int, int]
    validator_count: int
    stake_mode: str
    cross_shard_ratio: float
    poor_connectivity: bool = False
    risky_validators: bool = False
    hotspot_ratio: float = 0.0
    malicious_ratio: float = 0.0
    weak_mobile_ratio: float = 0.0


@dataclass
class RunOutput:
    scenario: str
    scenario_name: str
    run_id: int
    seed: int
    submitted_tx: int
    routed_tx: int
    finality_certificates: int
    receipts: int
    reward_events: int
    total_reward: int
    quarantine_events: int
    reconfiguration_events: int
    evidence_events: int
    active_validators: int
    quarantined_validators: int
    finality_success_rate: float
    receipt_success_rate: float
    throughput: float
    mean_finality_latency: float
    mean_receipt_latency: float
    cross_shard_ratio: float
    shard1_load: float
    shard2_load: float
    shard_load_std: float
    reward_gini: float
    reward_hhi: float
    owner_concentration: float
    nakamoto_coefficient: int
    malicious_committee_probability: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
