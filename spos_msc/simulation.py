"""Scenario runner for the SPoS-MSC prototype."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import DEFAULT_CONFIG, PrototypeConfig
from .metrics import gini, hhi, nakamoto_coefficient, reward_distribution_by_owner, reward_distribution_by_validator
from .models import RunOutput
from .msc import generate_receipts_rewards, reconfiguration_events, route_transactions, run_finality, shard_load_std
from .scenarios import SCENARIOS, generate_transactions, generate_validators
from .spos import form_vrf_committees, malicious_committee_probability, prepare_validators


def run_single_scenario(
    scenario_id: str,
    run_id: int,
    seed: int,
    config: PrototypeConfig = DEFAULT_CONFIG,
) -> RunOutput:
    if scenario_id not in SCENARIOS:
        raise ValueError(f"Unknown scenario_id={scenario_id}. Expected one of {sorted(SCENARIOS)}")

    scenario = SCENARIOS[scenario_id]
    rng = random.Random(seed)

    validators = generate_validators(scenario, rng)
    validators_by_id = {v.vid: v for v in validators}
    vid_to_owner = {v.vid: v.owner_id for v in validators}
    transactions = generate_transactions(scenario, rng, config.shard_count)

    active_scores, quarantined = prepare_validators(validators, config)
    committees = form_vrf_committees(active_scores, seed, config)

    base_load = {1: rng.uniform(20, 60), 2: rng.uniform(20, 55)}
    if scenario.hotspot_ratio:
        base_load[1] += 25
    routed, final_load, route_evidence = route_transactions(transactions, base_load, config)

    connectivity_penalty = 0.10 if scenario.poor_connectivity else 0.0
    certs, finality_evidence = run_finality(routed, committees, rng, config, connectivity_penalty)
    receipt_penalty = 0.02 + (0.06 if scenario.poor_connectivity else 0.0) + (0.04 if scenario.hotspot_ratio else 0.0)
    receipts, rewards, receipt_evidence = generate_receipts_rewards(certs, rng, config, receipt_penalty)

    reward_dist = reward_distribution_by_validator(rewards)
    owner_dist = reward_distribution_by_owner(rewards, vid_to_owner)
    reward_values = list(reward_dist.values())
    owner_values = list(owner_dist.values())

    submitted = len(transactions)
    routed_count = len(routed)
    cert_count = len(certs)
    receipt_count = len(receipts)
    finality_success = cert_count / submitted * 100 if submitted else 0.0
    receipt_success = receipt_count / submitted * 100 if submitted else 0.0
    avg_finality_latency = sum(c.finality_time for c in certs) / cert_count if cert_count else 0.0
    avg_receipt_latency = sum(r.receipt_time for r in receipts) / receipt_count if receipt_count else 0.0
    logical_window = max(config.base_time_window, submitted / 3)
    if scenario.scenario_id == "Q2":
        logical_window *= 0.85
    if scenario.scenario_id == "Q4":
        logical_window *= 1.25
    throughput = receipt_count / logical_window

    reconfigs = reconfiguration_events(final_load, config)
    evidence_events = len(route_evidence) + len(finality_evidence) + len(receipt_evidence)
    cross_count = sum(1 for tx in transactions if tx.cross_shard)
    malicious_prob = malicious_committee_probability(committees, validators_by_id, config)

    owner_total_reward = sum(owner_values)
    owner_concentration = max(owner_values) / owner_total_reward * 100 if owner_total_reward else 0.0

    return RunOutput(
        scenario=scenario.scenario_id,
        scenario_name=scenario.name,
        run_id=run_id,
        seed=seed,
        submitted_tx=submitted,
        routed_tx=routed_count,
        finality_certificates=cert_count,
        receipts=receipt_count,
        reward_events=len(rewards),
        total_reward=sum(r.reward for r in rewards),
        quarantine_events=len(quarantined),
        reconfiguration_events=reconfigs,
        evidence_events=evidence_events,
        active_validators=len(active_scores),
        quarantined_validators=len(quarantined),
        finality_success_rate=round(finality_success, 4),
        receipt_success_rate=round(receipt_success, 4),
        throughput=round(throughput, 4),
        mean_finality_latency=round(avg_finality_latency, 4),
        mean_receipt_latency=round(avg_receipt_latency, 4),
        cross_shard_ratio=round(cross_count / submitted * 100 if submitted else 0.0, 4),
        shard1_load=round(final_load.get(1, 0.0), 4),
        shard2_load=round(final_load.get(2, 0.0), 4),
        shard_load_std=round(shard_load_std(final_load), 4),
        reward_gini=round(gini(reward_values), 4),
        reward_hhi=round(hhi(reward_values), 4),
        owner_concentration=round(owner_concentration, 4),
        nakamoto_coefficient=nakamoto_coefficient(reward_values),
        malicious_committee_probability=round(malicious_prob, 4),
    )


def run_scenarios(
    scenario_ids: Iterable[str] = SCENARIOS.keys(),
    runs: int = 100,
    base_seed: int = 626,
    config: PrototypeConfig = DEFAULT_CONFIG,
) -> pd.DataFrame:
    rows = []
    for scenario_id in scenario_ids:
        for run_id in range(1, runs + 1):
            seed = base_seed + run_id + (abs(hash(scenario_id)) % 10000)
            rows.append(run_single_scenario(scenario_id, run_id, seed, config).as_dict())
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "submitted_tx",
        "finality_certificates",
        "receipts",
        "reward_events",
        "quarantine_events",
        "reconfiguration_events",
        "finality_success_rate",
        "receipt_success_rate",
        "throughput",
        "mean_finality_latency",
        "mean_receipt_latency",
        "cross_shard_ratio",
        "shard_load_std",
        "reward_gini",
        "reward_hhi",
        "owner_concentration",
        "nakamoto_coefficient",
        "malicious_committee_probability",
    ]
    grouped = df.groupby(["scenario", "scenario_name"], as_index=False)[metrics].agg(["mean", "std", "min", "max"])
    grouped.columns = ["_".join(col).rstrip("_") for col in grouped.columns.values]
    grouped = grouped.reset_index()
    return grouped


def export_results(df: pd.DataFrame, output_dir: Path, prefix: str = "spos_msc") -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / f"{prefix}_run_matrix.csv"
    summary_path = output_dir / f"{prefix}_summary.csv"
    excel_path = output_dir / f"{prefix}_results.xlsx"
    df.to_csv(raw_path, index=False)
    summary_df = summarize(df)
    summary_df.to_csv(summary_path, index=False)
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="RunMatrix", index=False)
        summary_df.to_excel(writer, sheet_name="ScenarioSummary", index=False)
    return {"run_matrix_csv": raw_path, "summary_csv": summary_path, "excel": excel_path}
