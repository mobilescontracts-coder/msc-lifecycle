#!/usr/bin/env python3
"""Validate and analyse the public SPoS-MSC v4 native CPN exports.

The script treats every complete CPN replication as one statistical observation.
Low, default, and high OFAT cells are independent repeated-run groups; run IDs
provide provenance and coverage identifiers rather than matched statistical pairs.

Outputs
-------
* Validation_Summary.csv
* v4_Default_Scenario_Statistics.csv
* v4_Sensitivity_Descriptive_Statistics.csv
* v4_Sensitivity_Primary_Responses.csv
* v4_Sensitivity_Independent_Contrasts.csv
* scenario and sensitivity figures in PDF and PNG formats

The script never interprets CPN logical throughput as public-network TPS.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

LEVEL_ORDER = ["LOW", "DEFAULT", "HIGH"]
SCENARIO_NAMES = {
    1: "Normal",
    2: "High load",
    3: "Cross-shard",
    4: "Poor connectivity",
    5: "Stake skew",
    6: "Risky/offline",
    7: "Hot shard",
}

FACTOR_META = {
    "WORKLOAD": {
        "label": "Transactions/run",
        "values": {"LOW": "16", "DEFAULT": "24", "HIGH": "40"},
        "primary": "logical_throughput",
        "primary_label": "Logical throughput",
    },
    "CROSS_SHARD_PCT": {
        "label": "Cross-shard demand",
        "values": {"LOW": "20%", "DEFAULT": "60%", "HIGH": "80%"},
        "primary": "mean_receipt_latency",
        "primary_label": "Receipt latency",
    },
    "REQUEST_OFFLINE_PCT": {
        "label": "Request disconnection",
        "values": {"LOW": "10%", "DEFAULT": "20%", "HIGH": "30%"},
        "primary": "finality_success_pct",
        "primary_label": "Finality success (%)",
    },
    "RECEIPT_DROP_PCT": {
        "label": "Receipt delivery drop",
        "values": {"LOW": "10%", "DEFAULT": "29%", "HIGH": "40%"},
        "primary": "receipt_success_pct",
        "primary_label": "Receipt success (%)",
    },
    "OWNER_CAP": {
        "label": "Owner-stake cap",
        "values": {"LOW": "1500", "DEFAULT": "3000", "HIGH": "6000"},
        "primary": "owner_concentration_pct",
        "primary_label": "Largest-owner reward share (%)",
    },
    "MOBILE_THRESHOLD": {
        "label": "Mobile-fitness threshold",
        "values": {"LOW": "25", "DEFAULT": "35", "HIGH": "65"},
        "primary": "eligible_validators",
        "primary_label": "Eligible validators",
    },
    "COMMITTEE_QUORUM": {
        "label": "Committee/quorum",
        "values": {"LOW": "3/2", "DEFAULT": "4/3", "HIGH": "5/4"},
        "primary": "committee_recoveries",
        "primary_label": "Committee recoveries/run",
    },
    "LOAD_THRESHOLD": {
        "label": "Load threshold",
        "values": {"LOW": "45", "DEFAULT": "55", "HIGH": "75"},
        "primary": "reconfiguration_events",
        "primary_label": "Reconfiguration events/run",
    },
}

RAW_REQUIRED = {
    "experiment_id", "factor_id", "level_id", "configuration", "scenario_id",
    "run_id", "base_seed", "model_time", "stop_code", "submitted_tx",
    "prepared_tx", "routed_tx", "cross_shard_tx", "shard_blocks",
    "eligible_validators", "active_committees", "committee_recoveries",
    "finality_certificates", "root_commitments", "receipts", "terminal_failures",
    "reward_events", "quarantine_events", "slashing_events",
    "reconfiguration_events", "evidence_count", "finality_latency_sum",
    "finality_latency_n", "receipt_latency_sum", "receipt_latency_n",
    "reward_gini_bp", "reward_hhi_bp", "nakamoto_coefficient",
    "owner_concentration_bp", "shard_load_std_bp",
}

SCENARIO_METRICS = [
    "finality_success_pct", "receipt_success_pct", "logical_throughput",
    "mean_finality_latency", "mean_receipt_latency", "cross_shard_ratio_pct",
    "reconfiguration_events", "shard_load_std", "eligible_validators",
    "committee_recoveries", "quarantine_events", "slashing_events",
    "reward_gini", "reward_hhi", "nakamoto_coefficient",
    "owner_concentration_pct",
]

SENSITIVITY_METRICS = [
    "submitted_tx", "prepared_success_pct", "finality_success_pct",
    "receipt_success_pct", "terminal_failure_pct", "cross_shard_ratio_pct",
    "logical_throughput", "mean_finality_latency", "mean_receipt_latency",
    "finality_receipt_gap_pp", "eligible_validators", "active_committees",
    "committee_recoveries", "reconfiguration_events", "shard_load_std",
    "reward_gini", "reward_hhi", "nakamoto_coefficient",
    "owner_concentration_pct", "quarantine_events", "slashing_events",
    "reward_events", "evidence_count", "model_time",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--default-csv", type=Path, required=True)
    parser.add_argument("--ofat-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--smoke-csv", type=Path)
    parser.add_argument("--pilot-csv", type=Path)
    return parser.parse_args()


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path)
    missing = sorted(RAW_REQUIRED.difference(frame.columns))
    if missing:
        raise ValueError(f"{path.name}: missing columns: {missing}")
    return derive_metrics(frame)


def safe_ratio(numerator: pd.Series, denominator: pd.Series, scale: float = 1.0) -> pd.Series:
    result = np.where(denominator.to_numpy() > 0,
                      scale * numerator.to_numpy() / denominator.to_numpy(),
                      np.nan)
    return pd.Series(result, index=numerator.index, dtype=float)


def derive_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    data["prepared_success_pct"] = safe_ratio(data["prepared_tx"], data["submitted_tx"], 100)
    data["finality_success_pct"] = safe_ratio(data["finality_certificates"], data["submitted_tx"], 100)
    data["receipt_success_pct"] = safe_ratio(data["receipts"], data["submitted_tx"], 100)
    data["terminal_failure_pct"] = safe_ratio(data["terminal_failures"], data["submitted_tx"], 100)
    data["cross_shard_ratio_pct"] = safe_ratio(data["cross_shard_tx"], data["submitted_tx"], 100)
    data["logical_throughput"] = safe_ratio(data["receipts"], data["model_time"], 1)
    data["mean_finality_latency"] = safe_ratio(data["finality_latency_sum"], data["finality_latency_n"], 1)
    data["mean_receipt_latency"] = safe_ratio(data["receipt_latency_sum"], data["receipt_latency_n"], 1)
    data["finality_receipt_gap_pp"] = data["finality_success_pct"] - data["receipt_success_pct"]
    data["reward_gini"] = data["reward_gini_bp"] / 100.0
    data["reward_hhi"] = data["reward_hhi_bp"] / 100.0
    data["owner_concentration_pct"] = data["owner_concentration_bp"] / 100.0
    data["shard_load_std"] = data["shard_load_std_bp"] / 100.0
    return data


def validate_frame(name: str, frame: pd.DataFrame, expected_rows: int,
                   group_cols: Sequence[str], groups: int, per_group: int) -> dict[str, object]:
    ordering = ~(
        (frame["receipts"] <= frame["root_commitments"])
        & (frame["root_commitments"] <= frame["finality_certificates"])
        & (frame["finality_certificates"] <= frame["shard_blocks"])
        & (frame["shard_blocks"] <= frame["routed_tx"])
        & (frame["routed_tx"] <= frame["prepared_tx"])
        & (frame["prepared_tx"] <= frame["submitted_tx"])
    )
    accounting = frame["receipts"] + frame["terminal_failures"] != frame["submitted_tx"]
    key_cols = list(group_cols) + ["run_id"]
    duplicate_count = int(frame.duplicated(key_cols).sum())
    grouped = frame.groupby(list(group_cols), dropna=False)
    bad_group_size = sum(len(group) != per_group for _, group in grouped)
    bad_run_ids = 0
    expected_ids = list(range(1, per_group + 1))
    for _, group in grouped:
        if sorted(group["run_id"].astype(int).tolist()) != expected_ids:
            bad_run_ids += 1
    complete_rows = int((frame["stop_code"] == "COMPLETE").sum())
    seeds = ";".join(str(int(x)) for x in sorted(frame["base_seed"].unique()))
    passed = (
        len(frame) == expected_rows
        and grouped.ngroups == groups
        and bad_group_size == 0
        and bad_run_ids == 0
        and complete_rows == len(frame)
        and int(ordering.sum()) == 0
        and int(accounting.sum()) == 0
        and duplicate_count == 0
    )
    return {
        "dataset": name,
        "rows": len(frame),
        "complete_rows": complete_rows,
        "groups": grouped.ngroups,
        "bad_group_sizes": bad_group_size,
        "run_id_group_violations": bad_run_ids,
        "lifecycle_violations": int(ordering.sum()),
        "terminal_accounting_violations": int(accounting.sum()),
        "duplicate_keys": duplicate_count,
        "base_seed_values": seeds,
        "status": "PASS" if passed else "FAIL",
    }


def describe(values: Iterable[float]) -> dict[str, float]:
    array = np.asarray(list(values), dtype=float)
    array = array[np.isfinite(array)]
    if len(array) == 0:
        return {key: math.nan for key in ("n", "mean", "sd", "median", "q1", "q3", "iqr", "min", "max", "ci_low", "ci_high", "ci_half")}
    n = len(array)
    mean = float(np.mean(array))
    sd = float(np.std(array, ddof=1)) if n > 1 else 0.0
    half = float(stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)) if n > 1 and sd > 0 else 0.0
    q1, q3 = np.quantile(array, [0.25, 0.75])
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "median": float(np.median(array)),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
        "ci_low": mean - half,
        "ci_high": mean + half,
        "ci_half": half,
    }


def welch_mean_difference(sample: np.ndarray, reference: np.ndarray) -> tuple[float, float, float]:
    sample = sample[np.isfinite(sample)]
    reference = reference[np.isfinite(reference)]
    difference = float(np.mean(sample) - np.mean(reference))
    variance_a = float(np.var(sample, ddof=1)) if len(sample) > 1 else 0.0
    variance_b = float(np.var(reference, ddof=1)) if len(reference) > 1 else 0.0
    se = math.sqrt(variance_a / len(sample) + variance_b / len(reference))
    if se == 0:
        return difference, difference, difference
    numerator = (variance_a / len(sample) + variance_b / len(reference)) ** 2
    denominator = 0.0
    if variance_a > 0:
        denominator += variance_a ** 2 / (len(sample) ** 2 * (len(sample) - 1))
    if variance_b > 0:
        denominator += variance_b ** 2 / (len(reference) ** 2 * (len(reference) - 1))
    degrees = numerator / denominator if denominator > 0 else math.inf
    critical = float(stats.t.ppf(0.975, degrees)) if math.isfinite(degrees) else 1.959963984540054
    return difference, difference - critical * se, difference + critical * se


def holm_adjust(p_values: Sequence[float]) -> list[float]:
    values = np.asarray(p_values, dtype=float)
    order = np.argsort(values)
    adjusted_sorted = np.empty_like(values)
    running = 0.0
    m = len(values)
    for rank, index in enumerate(order):
        candidate = min(1.0, (m - rank) * values[index])
        running = max(running, candidate)
        adjusted_sorted[index] = running
    return adjusted_sorted.tolist()


def scenario_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for scenario_id, group in frame.groupby("scenario_id"):
        for metric in SCENARIO_METRICS:
            stats_row = describe(group[metric])
            records.append({
                "scenario_id": int(scenario_id),
                "scenario": f"Q{int(scenario_id)}",
                "name": SCENARIO_NAMES[int(scenario_id)],
                "metric": metric,
                **stats_row,
            })
    return pd.DataFrame(records)


def sensitivity_statistics(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    descriptive: list[dict[str, object]] = []
    primary: list[dict[str, object]] = []
    contrasts: list[dict[str, object]] = []

    for factor_id, meta in FACTOR_META.items():
        factor_frame = frame[frame["factor_id"] == factor_id]
        if len(factor_frame) != 300:
            raise ValueError(f"{factor_id}: expected 300 rows, found {len(factor_frame)}")
        level_frames = {level: factor_frame[factor_frame["level_id"] == level] for level in LEVEL_ORDER}
        for level in LEVEL_ORDER:
            if len(level_frames[level]) != 100:
                raise ValueError(f"{factor_id}/{level}: expected 100 rows")
            for metric in SENSITIVITY_METRICS:
                descriptive.append({
                    "factor_id": factor_id,
                    "factor": meta["label"],
                    "level_id": level,
                    "level_value": meta["values"][level],
                    "metric": metric,
                    **describe(level_frames[level][metric]),
                })

        metric = meta["primary"]
        arrays = [level_frames[level][metric].to_numpy(dtype=float) for level in LEVEL_ORDER]
        h_stat, p_value = stats.kruskal(*arrays)
        epsilon = max(0.0, min(1.0, (float(h_stat) - len(LEVEL_ORDER) + 1) / (300 - len(LEVEL_ORDER))))
        means = [float(np.nanmean(array)) for array in arrays]
        primary.append({
            "factor_id": factor_id,
            "factor": meta["label"],
            "primary_metric": metric,
            "primary_metric_label": meta["primary_label"],
            "low_value": meta["values"]["LOW"],
            "default_value": meta["values"]["DEFAULT"],
            "high_value": meta["values"]["HIGH"],
            "low_mean": means[0],
            "default_mean": means[1],
            "high_mean": means[2],
            "kruskal_H": float(h_stat),
            "kruskal_p": float(p_value),
            "epsilon_squared": epsilon,
        })

        reference = level_frames["DEFAULT"][metric].to_numpy(dtype=float)
        for level in ("LOW", "HIGH"):
            sample = level_frames[level][metric].to_numpy(dtype=float)
            u_stat, p_raw = stats.mannwhitneyu(sample, reference, alternative="two-sided", method="auto")
            cliff_delta = 2.0 * float(u_stat) / (len(sample) * len(reference)) - 1.0
            mean_diff, ci_low, ci_high = welch_mean_difference(sample, reference)
            contrasts.append({
                "factor_id": factor_id,
                "factor": meta["label"],
                "level": level,
                "metric": metric,
                "U": float(u_stat),
                "p_raw": float(p_raw),
                "cliff_delta": cliff_delta,
                "mean_diff": mean_diff,
                "ci_low": ci_low,
                "ci_high": ci_high,
            })

    adjusted = holm_adjust([record["p_raw"] for record in contrasts])
    for record, p_holm in zip(contrasts, adjusted):
        record["p_holm"] = p_holm
    return pd.DataFrame(descriptive), pd.DataFrame(primary), pd.DataFrame(contrasts)


def save_plot(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close()


def make_figures(default: pd.DataFrame, ofat: pd.DataFrame, output_dir: Path,
                 primary: pd.DataFrame) -> None:
    figures = output_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    scenarios = sorted(default["scenario_id"].unique())
    labels = [f"Q{int(value)}" for value in scenarios]
    x = np.arange(len(scenarios))

    def scenario_mean_ci(metric: str) -> tuple[list[float], list[float]]:
        means, halves = [], []
        for scenario_id in scenarios:
            row = describe(default.loc[default["scenario_id"] == scenario_id, metric])
            means.append(row["mean"])
            halves.append(row["ci_half"])
        return means, halves

    plt.figure(figsize=(7.0, 4.2))
    means, halves = scenario_mean_ci("logical_throughput")
    plt.errorbar(x, means, yerr=halves, marker="o", capsize=4)
    plt.xticks(x, labels)
    plt.xlabel("Scenario")
    plt.ylabel("Receipts per logical-time unit")
    save_plot(figures / "Fig4_CPN_Logical_Throughput_v4")

    plt.figure(figsize=(7.0, 4.2))
    for metric, label, marker in [
        ("finality_success_pct", "Finality success", "o"),
        ("receipt_success_pct", "Receipt success", "s"),
    ]:
        means, halves = scenario_mean_ci(metric)
        plt.errorbar(x, means, yerr=halves, marker=marker, capsize=4, label=label)
    plt.xticks(x, labels)
    plt.xlabel("Scenario")
    plt.ylabel("Success (%)")
    plt.legend()
    save_plot(figures / "Fig5a_CPN_Finality_Receipt_Success_v4")

    plt.figure(figsize=(7.0, 4.2))
    for metric, label, marker in [
        ("mean_finality_latency", "Finality latency", "o"),
        ("mean_receipt_latency", "Receipt latency", "s"),
    ]:
        means, halves = scenario_mean_ci(metric)
        plt.errorbar(x, means, yerr=halves, marker=marker, capsize=4, label=label)
    plt.xticks(x, labels)
    plt.xlabel("Scenario")
    plt.ylabel("Logical-time units")
    plt.legend()
    save_plot(figures / "Fig5b_CPN_Finality_Receipt_Latency_v4")

    plt.figure(figsize=(7.0, 4.2))
    means, halves = scenario_mean_ci("cross_shard_ratio_pct")
    plt.errorbar(x, means, yerr=halves, marker="o", capsize=4)
    plt.xticks(x, labels)
    plt.xlabel("Scenario")
    plt.ylabel("Cross-shard transactions (%)")
    save_plot(figures / "Fig6a_CPN_Cross_Shard_Ratio_v4")

    plt.figure(figsize=(7.0, 4.2))
    for metric, label, marker in [
        ("reconfiguration_events", "Reconfigurations/run", "o"),
        ("shard_load_std", "Shard-load SD", "s"),
    ]:
        means, halves = scenario_mean_ci(metric)
        plt.errorbar(x, means, yerr=halves, marker=marker, capsize=4, label=label)
    plt.xticks(x, labels)
    plt.xlabel("Scenario")
    plt.ylabel("Run-level mean")
    plt.legend()
    save_plot(figures / "Fig6b_CPN_Reconfiguration_Load_Imbalance_v4")

    plt.figure(figsize=(7.0, 4.2))
    for metric, label, marker in [
        ("reward_gini", "Reward Gini", "o"),
        ("reward_hhi", "Reward HHI", "s"),
    ]:
        means, halves = scenario_mean_ci(metric)
        plt.errorbar(x, means, yerr=halves, marker=marker, capsize=4, label=label)
    plt.xticks(x, labels)
    plt.xlabel("Scenario")
    plt.ylabel("Concentration index (0-100)")
    plt.legend()
    save_plot(figures / "Fig7_CPN_Reward_Gini_HHI_v4")

    ordered = primary.sort_values("epsilon_squared")
    plt.figure(figsize=(7.4, 4.8))
    plt.barh(ordered["factor"], ordered["epsilon_squared"])
    plt.xlabel(r"Kruskal--Wallis $\epsilon^2$ for the primary response")
    plt.xlim(0, 1.05)
    save_plot(figures / "Fig8_Sensitivity_Primary_Effect_Size_v4")

    mobile = ofat[ofat["factor_id"] == "MOBILE_THRESHOLD"]
    mobile_levels = [mobile[mobile["level_id"] == level] for level in LEVEL_ORDER]
    values = [FACTOR_META["MOBILE_THRESHOLD"]["values"][level] for level in LEVEL_ORDER]
    x_mobile = np.arange(3)

    plt.figure(figsize=(6.4, 4.2))
    for metric, label, marker in [
        ("finality_success_pct", "Finality success", "o"),
        ("receipt_success_pct", "Receipt success", "s"),
        ("eligible_validators", "Eligible validators", "^")
    ]:
        means = [describe(level[metric])["mean"] for level in mobile_levels]
        halves = [describe(level[metric])["ci_half"] for level in mobile_levels]
        plt.errorbar(x_mobile, means, yerr=halves, marker=marker, capsize=4, label=label)
    plt.xticks(x_mobile, values)
    plt.xlabel("Mobile-fitness threshold")
    plt.ylabel("Run-level mean")
    plt.legend()
    save_plot(figures / "Fig9a_Sensitivity_MobileThreshold_Success_v4")

    plt.figure(figsize=(6.4, 4.2))
    for metric, label, marker in [
        ("reward_gini", "Reward Gini", "o"),
        ("reward_hhi", "Reward HHI", "s"),
        ("owner_concentration_pct", "Largest-owner share", "^")
    ]:
        means = [describe(level[metric])["mean"] for level in mobile_levels]
        halves = [describe(level[metric])["ci_half"] for level in mobile_levels]
        plt.errorbar(x_mobile, means, yerr=halves, marker=marker, capsize=4, label=label)
    plt.xticks(x_mobile, values)
    plt.xlabel("Mobile-fitness threshold")
    plt.ylabel("Metric value (0-100 scale)")
    plt.legend()
    save_plot(figures / "Fig9b_Sensitivity_MobileThreshold_Concentration_v4")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    default = read_csv(args.default_csv)
    ofat = read_csv(args.ofat_csv)
    validation_rows = [
        validate_frame("default", default, 700, ["scenario_id"], 7, 100),
        validate_frame("ofat", ofat, 2400, ["factor_id", "level_id"], 24, 100),
    ]
    if args.smoke_csv:
        smoke = read_csv(args.smoke_csv)
        validation_rows.insert(0, validate_frame("smoke", smoke, 2,
                                                  ["experiment_id", "factor_id", "level_id"], 1, 2))
    if args.pilot_csv:
        pilot = read_csv(args.pilot_csv)
        insertion = 1 if args.smoke_csv else 0
        validation_rows.insert(insertion, validate_frame("pilot", pilot, 72,
                                                          ["factor_id", "level_id"], 24, 3))

    validation = pd.DataFrame(validation_rows)
    if not (validation["status"] == "PASS").all():
        validation.to_csv(args.output_dir / "Validation_Summary.csv", index=False)
        raise SystemExit("Validation fails; inspect Validation_Summary.csv before analysis.")

    scenarios = scenario_statistics(default)
    descriptive, primary, contrasts = sensitivity_statistics(ofat)

    validation.to_csv(args.output_dir / "Validation_Summary.csv", index=False)
    scenarios.to_csv(args.output_dir / "v4_Default_Scenario_Statistics.csv", index=False)
    descriptive.to_csv(args.output_dir / "v4_Sensitivity_Descriptive_Statistics.csv", index=False)
    primary.to_csv(args.output_dir / "v4_Sensitivity_Primary_Responses.csv", index=False)
    contrasts.to_csv(args.output_dir / "v4_Sensitivity_Independent_Contrasts.csv", index=False)
    make_figures(default, ofat, args.output_dir, primary)

    print("PASS: native matrices satisfy the configured integrity checks.")
    print(f"Outputs: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
