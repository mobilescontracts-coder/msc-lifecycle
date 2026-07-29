#!/usr/bin/env python3
"""Rebuild scenario and aggregate summaries from the prototype API run matrix."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

T_975_DF99 = 1.9842169515086827
METRICS = [
    "api_elapsed_ms",
    "real_submitted_tx_per_sec",
    "real_receipts_per_sec",
    "finality_success_rate",
    "receipt_success_rate",
    "mean_finality_latency_logical",
    "mean_receipt_latency_logical",
    "cross_shard_ratio",
    "shard_load_std",
    "reward_gini",
    "reward_hhi",
    "owner_concentration",
    "nakamoto_coefficient",
    "reconfiguration_events",
    "quarantine_events",
]


def describe(series: pd.Series) -> dict[str, float | int]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    n = int(values.size)
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

    source = root / "data/raw/prototype/realtime_api_run_matrix.csv"
    runs = pd.read_csv(source)
    if len(runs) != 700:
        raise ValueError(f"Expected 700 prototype rows, found {len(runs)}")
    counts = runs.groupby("scenario").size().to_dict()
    if counts != {f"Q{i}": 100 for i in range(1, 8)}:
        raise ValueError(f"Unbalanced scenario counts: {counts}")

    long_rows: list[dict[str, object]] = []
    wide_rows: list[dict[str, object]] = []
    for scenario, group in runs.groupby("scenario", sort=True):
        wide: dict[str, object] = {
            "scenario": scenario,
            "scenario_name": group["scenario_name"].iloc[0],
            "runs": len(group),
        }
        for metric in METRICS:
            stats = describe(group[metric])
            long_rows.append(
                {
                    "scenario": scenario,
                    "scenario_name": group["scenario_name"].iloc[0],
                    "metric": metric,
                    **stats,
                }
            )
            for key in ("mean", "sd", "ci95_half_width", "median", "q1", "q3"):
                wide[f"{metric}_{key}"] = stats[key]
        wide_rows.append(wide)

    pd.DataFrame(long_rows).to_csv(output / "prototype_summary_long.csv", index=False)
    pd.DataFrame(wide_rows).to_csv(output / "prototype_scenario_summary.csv", index=False)

    transactions = int(runs["submitted_tx"].sum())
    finality = int(runs["finality_certificates"].sum())
    receipts = int(runs["receipts"].sum())
    elapsed = float(runs["api_elapsed_seconds"].sum())
    aggregate = {
        "executions": int(len(runs)),
        "transactions": transactions,
        "routed_transactions": int(runs["routed_tx"].sum()),
        "finality_certificates": finality,
        "receipts": receipts,
        "reward_events": int(runs["reward_events"].sum()),
        "weighted_finality_success_percent": 100.0 * finality / transactions,
        "weighted_receipt_success_percent": 100.0 * receipts / transactions,
        "sum_api_elapsed_seconds": elapsed,
        "receipts_per_sum_api_seconds": receipts / elapsed,
        "provenance": "controlled single-host prototype API benchmark; not public-network throughput",
    }
    # Preserve the measured full sequential wall-clock value from the benchmark log.
    kpis = pd.read_csv(root / "data/raw/prototype/realtime_overall_kpis.csv")
    lookup = dict(zip(kpis["parameter"], kpis["value"], strict=False))
    for source_key, output_key in (
        ("sequential_api_wall_clock_seconds", "measured_sequential_wall_clock_seconds"),
        ("sequential_real_receipts_per_sec", "measured_sequential_receipts_per_second"),
        ("sequential_real_submitted_tx_per_sec", "measured_sequential_transactions_per_second"),
    ):
        if source_key in lookup:
            aggregate[output_key] = float(lookup[source_key])

    (output / "prototype_aggregate.json").write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "evidence_type": "prototype_benchmark",
        "source": source.relative_to(root).as_posix(),
        "run_count": len(runs),
        "scenario_counts": counts,
        "warning": "Throughput values describe a controlled single-host lifecycle benchmark, not a public blockchain network.",
    }
    (output / "prototype_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote prototype reproduction outputs to {output}")
    print(json.dumps(aggregate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
