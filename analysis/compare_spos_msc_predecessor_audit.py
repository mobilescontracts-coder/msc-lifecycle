#!/usr/bin/env python3
"""Audit public v4 default outputs against the archived public v3 matrix.

The audit separates core lifecycle totals from stochastic diagnostic totals.
It does not label v4 as exactly equivalent unless every compared field agrees.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

CORE = [
    "submitted_tx", "prepared_tx", "routed_tx", "shard_blocks",
    "finality_certificates", "root_commitments", "receipts", "terminal_failures",
]
DIAGNOSTIC = [
    "cross_shard_tx", "reward_events", "committee_recoveries",
    "quarantine_events", "slashing_events", "reconfiguration_events",
    "evidence_count",
]
ROW_FIELDS = [
    "scenario_id", "run_id", "base_seed", "model_time", "stop_code", *CORE,
    *DIAGNOSTIC, "eligible_validators", "active_committees",
    "finality_latency_sum", "finality_latency_n", "receipt_latency_sum",
    "receipt_latency_n", "reward_gini_bp", "reward_hhi_bp",
    "nakamoto_coefficient", "owner_concentration_bp", "shard_load_std_bp",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predecessor", required=True, type=Path)
    parser.add_argument("--v4", required=True, type=Path)
    parser.add_argument("--aggregate-output", type=Path,
                        default=Path("v4_Default_Configuration_Aggregate_Audit.csv"))
    parser.add_argument("--row-output", type=Path,
                        default=Path("v4_Predecessor_Row_Differences.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predecessor = pd.read_csv(args.predecessor)
    current = pd.read_csv(args.v4)
    for label, frame in (("v3", predecessor), ("v4", current)):
        missing = [column for column in ROW_FIELDS if column not in frame.columns]
        if missing:
            raise SystemExit(f"{label}: missing columns {missing}")
        if len(frame) != 700:
            raise SystemExit(f"{label}: expected 700 rows, found {len(frame)}")

    aggregate_rows = []
    for metric in CORE + DIAGNOSTIC:
        old_value = int(predecessor[metric].sum())
        new_value = int(current[metric].sum())
        aggregate_rows.append({
            "metric": metric,
            "category": "core_lifecycle" if metric in CORE else "stochastic_diagnostic",
            "archived_v3": old_value,
            "v4_default_audit": new_value,
            "difference": new_value - old_value,
            "exact_match": old_value == new_value,
        })
    aggregate = pd.DataFrame(aggregate_rows)
    aggregate.to_csv(args.aggregate_output, index=False)

    old = predecessor[ROW_FIELDS].sort_values(["scenario_id", "run_id"]).reset_index(drop=True)
    new = current[ROW_FIELDS].sort_values(["scenario_id", "run_id"]).reset_index(drop=True)
    unequal = old.ne(new)
    row_records = []
    for row_index, column in zip(*unequal.to_numpy().nonzero()):
        row_records.append({
            "scenario_id": int(old.at[row_index, "scenario_id"]),
            "run_id": int(old.at[row_index, "run_id"]),
            "column": column if isinstance(column, str) else ROW_FIELDS[column],
            "archived_v3": old.iloc[row_index, column],
            "v4": new.iloc[row_index, column],
        })
    # numpy.nonzero returns numeric column positions; rebuild safely.
    if row_records:
        corrected = []
        for row_index in range(len(old)):
            for column in ROW_FIELDS:
                if unequal.at[row_index, column]:
                    corrected.append({
                        "scenario_id": int(old.at[row_index, "scenario_id"]),
                        "run_id": int(old.at[row_index, "run_id"]),
                        "column": column,
                        "archived_v3": old.at[row_index, column],
                        "v4": new.at[row_index, column],
                    })
        pd.DataFrame(corrected).to_csv(args.row_output, index=False)
    else:
        pd.DataFrame(columns=["scenario_id", "run_id", "column", "archived_v3", "v4"]).to_csv(args.row_output, index=False)

    core_ok = bool(aggregate.loc[aggregate["category"] == "core_lifecycle", "exact_match"].all())
    exact = bool(aggregate["exact_match"].all() and not unequal.any().any())
    print(f"Core lifecycle aggregate audit: {'PASS' if core_ok else 'FAIL'}")
    print(f"Exact row/field equivalence: {'PASS' if exact else 'NOT ESTABLISHED'}")
    print(f"Aggregate report: {args.aggregate_output}")
    print(f"Row-level report: {args.row_output}")
    if not core_ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
