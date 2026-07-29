"""Scenario generation for the Qtum-inspired SPoS-MSC prototype."""

from __future__ import annotations

import random
from .models import MobileTransaction, ScenarioConfig, Validator

SCENARIOS: dict[str, ScenarioConfig] = {
    "Q1": ScenarioConfig(
        scenario_id="Q1",
        name="Normal Qtum mobile contract request",
        tx_count_range=(180, 260),
        validator_count=12,
        stake_mode="balanced",
        cross_shard_ratio=0.12,
    ),
    "Q2": ScenarioConfig(
        scenario_id="Q2",
        name="High-load Qtum mobile dApp",
        tx_count_range=(360, 520),
        validator_count=16,
        stake_mode="moderate",
        cross_shard_ratio=0.19,
    ),
    "Q3": ScenarioConfig(
        scenario_id="Q3",
        name="Cross-contract/cross-shard Qtum request",
        tx_count_range=(220, 340),
        validator_count=14,
        stake_mode="moderate",
        cross_shard_ratio=0.47,
    ),
    "Q4": ScenarioConfig(
        scenario_id="Q4",
        name="Poor mobile connectivity",
        tx_count_range=(180, 300),
        validator_count=12,
        stake_mode="moderate",
        cross_shard_ratio=0.15,
        poor_connectivity=True,
        weak_mobile_ratio=0.25,
    ),
    "Q5": ScenarioConfig(
        scenario_id="Q5",
        name="Stake-skewed validator set",
        tx_count_range=(260, 380),
        validator_count=14,
        stake_mode="skewed",
        cross_shard_ratio=0.16,
    ),
    "Q6": ScenarioConfig(
        scenario_id="Q6",
        name="Risky/offline validator case",
        tx_count_range=(220, 330),
        validator_count=14,
        stake_mode="moderate",
        cross_shard_ratio=0.19,
        risky_validators=True,
        malicious_ratio=0.25,
    ),
    "Q7": ScenarioConfig(
        scenario_id="Q7",
        name="Hot-shard Qtum workload",
        tx_count_range=(300, 460),
        validator_count=16,
        stake_mode="moderate",
        cross_shard_ratio=0.23,
        hotspot_ratio=0.70,
    ),
}


def generate_validators(cfg: ScenarioConfig, rng: random.Random) -> list[Validator]:
    validators: list[Validator] = []
    for i in range(1, cfg.validator_count + 1):
        owner_id = i if cfg.stake_mode != "stake_split" else (1 if i <= 4 else i)
        if cfg.stake_mode == "balanced":
            stake = rng.randint(70, 170)
        elif cfg.stake_mode == "skewed":
            stake = rng.randint(60, 160)
            if i == 1:
                stake = rng.randint(4000, 6000)
            if i == 2:
                stake = rng.randint(800, 1600)
        else:
            stake = rng.randint(40, 600)

        mobile_fitness = rng.randint(60, 98)
        attack_risk = rng.randint(0, 35)

        if cfg.weak_mobile_ratio and rng.random() < cfg.weak_mobile_ratio:
            mobile_fitness = rng.randint(10, 35)
        if cfg.malicious_ratio and rng.random() < cfg.malicious_ratio:
            attack_risk = rng.randint(70, 95)

        validators.append(
            Validator(
                vid=i,
                owner_id=owner_id,
                stake=stake,
                mobile_fitness=mobile_fitness,
                attack_risk=attack_risk,
                availability=rng.randint(70, 100),
            )
        )
    return validators


def generate_transactions(cfg: ScenarioConfig, rng: random.Random, shard_count: int) -> list[MobileTransaction]:
    count = rng.randint(*cfg.tx_count_range)
    transactions: list[MobileTransaction] = []
    for offset in range(count):
        tx_id = 100000 + offset
        if cfg.hotspot_ratio and rng.random() < cfg.hotspot_ratio:
            contract_id = rng.choice([1, 3, 5, 7])  # maps frequently to one shard in simple modulo routing
        else:
            contract_id = rng.randint(1, 1000)
        cross_shard = rng.random() < cfg.cross_shard_ratio
        source_shard = 1 + (contract_id % shard_count)
        if cross_shard:
            target_shard = 1 + ((source_shard) % shard_count)
        else:
            target_shard = source_shard
        transactions.append(
            MobileTransaction(
                tx_id=tx_id,
                sender=f"mobile-{rng.randint(1, 200)}",
                contract_id=contract_id,
                payload_size=rng.randint(1, 8),
                cross_shard=cross_shard,
                source_shard=source_shard,
                target_shard=target_shard,
            )
        )
    return transactions
