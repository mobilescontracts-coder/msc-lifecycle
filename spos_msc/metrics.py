"""Metric functions used for evaluation and manuscript-ready output matrices."""

from __future__ import annotations

from collections import defaultdict
from math import isclose
from statistics import mean, pstdev


def gini(values: list[float]) -> float:
    """Return Gini coefficient on a 0--100 scale."""
    vals = sorted([float(v) for v in values if v >= 0])
    if not vals or isclose(sum(vals), 0.0):
        return 0.0
    n = len(vals)
    weighted_sum = sum((i + 1) * v for i, v in enumerate(vals))
    return ((2 * weighted_sum) / (n * sum(vals)) - (n + 1) / n) * 100


def hhi(values: list[float]) -> float:
    """Return Herfindahl-Hirschman Index on a 0--100 scale."""
    total = float(sum(v for v in values if v >= 0))
    if total <= 0:
        return 0.0
    shares = [(v / total) for v in values if v >= 0]
    return sum(s * s for s in shares) * 100


def nakamoto_coefficient(values: list[float], threshold: float = 1 / 3) -> int:
    """Count actors required to exceed a control threshold."""
    total = float(sum(v for v in values if v >= 0))
    if total <= 0:
        return 0
    cumulative = 0.0
    for i, value in enumerate(sorted(values, reverse=True), start=1):
        cumulative += value / total
        if cumulative >= threshold:
            return i
    return len(values)


def summarize_numeric(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": float(mean(values)),
        "std": float(pstdev(values)),
        "min": float(min(values)),
        "max": float(max(values)),
    }


def reward_distribution_by_validator(rewards) -> dict[int, int]:
    dist: dict[int, int] = defaultdict(int)
    for event in rewards:
        dist[event.validator_id] += event.reward
    return dict(dist)


def reward_distribution_by_owner(rewards, vid_to_owner: dict[int, int]) -> dict[int, int]:
    dist: dict[int, int] = defaultdict(int)
    for event in rewards:
        owner_id = vid_to_owner.get(event.validator_id, event.validator_id)
        dist[owner_id] += event.reward
    return dict(dist)
