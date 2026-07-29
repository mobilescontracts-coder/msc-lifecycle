"""Configuration constants for the SPoS-MSC research prototype.

These values are deliberately close to the integrated CPN model semantics, while
remaining easy to tune for scenario experiments.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PrototypeConfig:
    min_stake: int = 10
    owner_stake_cap: int = 1000
    mobile_fitness_min: int = 28
    attack_threshold: int = 70
    score_min: float = 30.0
    shard_count: int = 2
    committee_size: int = 3
    min_committee_size: int = 2
    rebalance_threshold: int = 75
    reward_finality: int = 5
    reward_receipt: int = 2
    proposer_bonus: int = 2
    voter_reward: int = 3
    edge_latency: int = 2
    block_time: int = 5
    finality_latency: int = 10
    receipt_latency: int = 4
    base_time_window: int = 100


DEFAULT_CONFIG = PrototypeConfig()
