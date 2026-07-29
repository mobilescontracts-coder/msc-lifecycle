#!/usr/bin/env python3
"""Rebuild manuscript CPN-proxy summaries from the Q1–Q7 output matrices.

The source workbook explicitly states that it was produced by a model-faithful
Python execution of the integrated CPN transition semantics because native CPN
Tools was unavailable in that runtime.  The script preserves this provenance
and must not be used to relabel these results as native CPN monitor exports.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

T_975_DF99 = 1.9842169515086827
PRIMARY_WORKBOOK = "SPoS_MSC_Q1_Q7_CPN_Output_Matrices_100runs.xlsx"

# source column -> stable repository metric name
METRICS = {
    "FinalitySuccessPct": "finality_success_percent",
    "ReceiptSuccessPct": "receipt_success_percent",
    "Throughput": "throughput_logical",
    "MeanFinalityLatency": "finality_latency_logical",
    "MeanReceiptLatency": "receipt_latency_logical",
    "P_MSC2_RoutedShardMempool[CrossShardTx]": "cross_shard_transactions",
    "P_SP6_ShardLoad[LoadStd]": "shard_load_std",
    "P_SP8_ReconfigurationEvents[Count]": "reconfiguration_events",
    "P_SP9_QuarantineAndSlashingLog[Count]": "quarantine_events",
    "RewardGini": "reward_gini",
    "RewardHHI": "reward_hhi",
    "RewardNakamoto": "nakamoto_coefficient",
    "OwnerConcentrationPct": "owner_concentration_percent",
}


def describe(series: pd.Series) -> dict[str, float | int]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    n = int(values.size)
    if n == 0:
        raise ValueError("Cannot summarise an empty metric series")
    mean = float(values.mean())
    sd = float(values.std(ddof=1)) if n > 1 else 0.0
    half = T_975_DF99 * sd / np.sqrt(n) if n > 1 else 0.0
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "ci95_half_width": float(half),
        "ci95_lower": float(mean - half),
        "ci95_upper": float(mean + half),
        "median": float(values.median()),
        "q1": float(values.quantile(0.25)),
        "q3": float(values.quantile(0.75)),
        "min": float(values.min()),
        "max": float(values.max()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo.resolve()
    output = args.output or (root / "outputs" / "reproduced")
    output.mkdir(parents=True, exist_ok=True)

    workbook = root / "data" / "raw" / "cpn_proxy" / PRIMARY_WORKBOOK
    if not workbook.is_file():
        raise FileNotFoundError(workbook)
    runs = pd.read_excel(workbook, sheet_name="AllRuns_OutputMatrix")
    if len(runs) != 700:
        raise ValueError(f"Expected 700 rows, found {len(runs)}")
    counts = runs.groupby("Scenario").size().to_dict()
    expected = {f"Q{i}": 100 for i in range(1, 8)}
    if counts != expected:
        raise ValueError(f"Unbalanced scenario counts: {counts}")

    runs = runs.copy()
    runs.insert(0, "source_workbook", PRIMARY_WORKBOOK)
    runs.insert(1, "evidence_type", "cpn_proxy")
    runs["SubmittedTx"] = (
        runs["P_MSC2_RoutedShardMempool[Shard1Tx]"]
        + runs["P_MSC2_RoutedShardMempool[Shard2Tx]"]
    )
    runs["CrossShardRatioPct"] = (
        100.0 * runs["P_MSC2_RoutedShardMempool[CrossShardTx]"] / runs["SubmittedTx"]
    )
    runs.to_csv(output / "cpn_proxy_run_matrix.csv", index=False)

    metric_map = dict(METRICS)
    metric_map["CrossShardRatioPct"] = "cross_shard_ratio_percent"

    long_rows: list[dict[str, object]] = []
    wide_rows: list[dict[str, object]] = []
    for scenario, group in runs.groupby("Scenario", sort=True):
        wide: dict[str, object] = {"scenario": scenario, "runs": int(len(group))}
        for source_column, metric_name in metric_map.items():
            stats = describe(group[source_column])
            long_rows.append({"scenario": scenario, "metric": metric_name, **stats})
            for key in ("mean", "sd", "ci95_half_width", "median", "q1", "q3"):
                wide[f"{metric_name}_{key}"] = stats[key]
        wide_rows.append(wide)
    pd.DataFrame(long_rows).to_csv(output / "cpn_proxy_summary_long.csv", index=False)
    pd.DataFrame(wide_rows).to_csv(output / "cpn_proxy_scenario_summary.csv", index=False)

    transactions = int(runs["SubmittedTx"].sum())
    finality = int(runs["P_SP4_FinalityCertificates[Total]"].sum())
    receipts = int(runs["P_MSC3_ReceiptQueue[Total]"].sum())
    # Each run's logical duration is receipts / throughput. Summing durations
    # before dividing preserves the manuscript's aggregate throughput definition.
    logical_duration = float(
        (runs["P_MSC3_ReceiptQueue[Total]"] / runs["Throughput"]).sum()
    )
    aggregate = {
        "runs": int(len(runs)),
        "transactions": transactions,
        "finality_certificates": finality,
        "receipts": receipts,
        "total_reward_amount": int(runs["P_SP5_RewardEvents[TotalReward]"].sum()),
        "evidence_tokens": int(runs["P_SP10_IntegratedEvidenceLog[Tokens]"].sum()),
        "reconfiguration_events": int(runs["P_SP8_ReconfigurationEvents[Count]"].sum()),
        "quarantine_events": int(runs["P_SP9_QuarantineAndSlashingLog[Count]"].sum()),
        "cross_shard_transactions": int(runs["P_MSC2_RoutedShardMempool[CrossShardTx]"].sum()),
        "weighted_finality_success_percent": 100.0 * finality / transactions,
        "weighted_receipt_success_percent": 100.0 * receipts / transactions,
        "weighted_cross_shard_ratio_percent": 100.0
        * int(runs["P_MSC2_RoutedShardMempool[CrossShardTx]"].sum())
        / transactions,
        "weighted_throughput_logical": receipts / logical_duration,
        "mean_finality_latency": float(runs["MeanFinalityLatency"].mean()),
        "mean_receipt_latency": float(runs["MeanReceiptLatency"].mean()),
        "mean_reward_gini": float(runs["RewardGini"].mean()),
        "mean_reward_hhi": float(runs["RewardHHI"].mean()),
        "mean_owner_concentration_percent": float(runs["OwnerConcentrationPct"].mean()),
        "provenance": "Model-faithful Python execution of integrated CPN semantics; not native CPN Tools monitor exports",
    }
    (output / "cpn_proxy_aggregate.json").write_text(
        json.dumps(aggregate, indent=2) + "\n", encoding="utf-8"
    )

    provenance = {
        "evidence_type": "cpn_proxy",
        "native_cpn_tools_export": False,
        "source": workbook.relative_to(root).as_posix(),
        "sheet": "AllRuns_OutputMatrix",
        "run_count": int(len(runs)),
        "scenario_counts": counts,
        "warning": "Do not cite these files as native CPN Tools monitor output.",
    }
    (output / "cpn_proxy_provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Wrote CPN-proxy reproduction outputs to {output}")
    print(json.dumps(aggregate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
