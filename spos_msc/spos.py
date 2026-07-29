"""SPoS consensus-control logic.

The logic is intentionally transparent and deterministic so that it can be mapped back
from prototype traces to the integrated CPN places and transitions.
"""

from __future__ import annotations

import hashlib
import math
import random
from collections import defaultdict

from .config import PrototypeConfig
from .models import CommitteeMember, Validator, ValidatorScore


def _stable_hash(*parts: object) -> int:
    payload = "|".join(str(p) for p in parts).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest(), 16)


def prepare_validators(
    validators: list[Validator], config: PrototypeConfig
) -> tuple[list[ValidatorScore], list[ValidatorScore]]:
    """Apply owner-aware stake cap, mobile fitness, risk filtering and scoring."""
    owner_total: dict[int, int] = defaultdict(int)
    for validator in validators:
        owner_total[validator.owner_id] += validator.stake

    active: list[ValidatorScore] = []
    quarantined: list[ValidatorScore] = []

    for validator in validators:
        total = owner_total[validator.owner_id]
        cap_ratio = min(total, config.owner_stake_cap) / total if total else 0
        owner_adjusted = validator.stake * cap_ratio
        stake_component = math.sqrt(max(owner_adjusted, 0)) * 3.0
        score = stake_component + validator.mobile_fitness - validator.attack_risk * 0.6

        reasons: list[str] = []
        if validator.stake < config.min_stake:
            reasons.append("stake_below_minimum")
        if validator.mobile_fitness < config.mobile_fitness_min:
            reasons.append("mobile_fitness_below_threshold")
        if validator.attack_risk >= config.attack_threshold:
            reasons.append("attack_risk_above_threshold")
        if score < config.score_min:
            reasons.append("score_below_minimum")

        eligible = not reasons
        score_token = ValidatorScore(
            vid=validator.vid,
            owner_id=validator.owner_id,
            raw_stake=validator.stake,
            owner_total_stake=total,
            owner_adjusted_stake=owner_adjusted,
            mobile_fitness=validator.mobile_fitness,
            attack_risk=validator.attack_risk,
            score=round(score, 3),
            eligible=eligible,
            reason="eligible" if eligible else ";".join(reasons),
        )
        if eligible:
            active.append(score_token)
        else:
            quarantined.append(score_token)

    return active, quarantined


def form_vrf_committees(
    active_scores: list[ValidatorScore],
    seed: int,
    config: PrototypeConfig,
) -> dict[int, list[CommitteeMember]]:
    """Form reproducible shard committees using VRF-style seeded ranking."""
    committees: dict[int, list[CommitteeMember]] = {}
    for shard_id in range(1, config.shard_count + 1):
        ranked: list[tuple[int, ValidatorScore]] = []
        for score in active_scores:
            value = _stable_hash(seed, shard_id, score.vid, round(score.score, 2))
            # Higher active score lowers the rank value, increasing selection probability.
            rank = value // max(int(score.score), 1)
            ranked.append((rank, score))
        ranked.sort(key=lambda item: item[0])
        selected = ranked[: config.committee_size]
        members = []
        for idx, (rank, score) in enumerate(selected):
            role = "proposer" if idx == 0 else "voter"
            members.append(
                CommitteeMember(
                    shard_id=shard_id,
                    validator_id=score.vid,
                    role=role,
                    selection_hash=rank,
                )
            )
        committees[shard_id] = members
    return committees


def committee_is_viable(members: list[CommitteeMember], config: PrototypeConfig) -> bool:
    return len({m.validator_id for m in members}) >= config.min_committee_size


def malicious_committee_probability(
    committees: dict[int, list[CommitteeMember]],
    validators_by_id: dict[int, Validator],
    config: PrototypeConfig,
) -> float:
    """Estimate percentage of committees containing risky majority members."""
    if not committees:
        return 0.0
    risky_count = 0
    for members in committees.values():
        risky_members = [
            m for m in members
            if validators_by_id.get(m.validator_id)
            and validators_by_id[m.validator_id].attack_risk >= config.attack_threshold
        ]
        if members and len(risky_members) / len(members) >= 1 / 3:
            risky_count += 1
    return (risky_count / len(committees)) * 100


def select_finality_participants(
    committee: list[CommitteeMember], rng: random.Random
) -> tuple[int, tuple[int, ...]]:
    """Select proposer and voters from a committee."""
    if not committee:
        raise ValueError("Cannot select finality participants from an empty committee.")
    proposer = next((m.validator_id for m in committee if m.role == "proposer"), committee[0].validator_id)
    voters = [m.validator_id for m in committee if m.validator_id != proposer]
    rng.shuffle(voters)
    return proposer, tuple(voters[:2])
