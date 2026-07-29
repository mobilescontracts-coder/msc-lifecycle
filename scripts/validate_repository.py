#!/usr/bin/env python3
"""Validate repository completeness, data shape, and headline metric consistency."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

CANONICAL_CPN = "SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn"


@dataclass
class Check:
    level: str
    name: str
    detail: str


def check_file(root: Path, relative: str, required: bool = True) -> Check:
    path = root / relative
    if path.is_file():
        return Check("PASS", relative, "present")
    return Check("FAIL" if required else "WARN", relative, "missing")


def approximate(actual: float, expected: float, tolerance: float = 1e-3) -> bool:
    return abs(float(actual) - float(expected)) <= tolerance


def validate_cpn_version(path: Path) -> Check:
    if not path.is_file():
        return Check("WARN", "integrated CPN model", "not imported; see docs/RELEASE_BLOCKERS.md")
    text = path.read_bytes().decode("iso-8859-1", errors="replace")
    match = re.search(r'<generator\s+tool="CPN Tools"\s+version="([^"]+)"', text)
    if not match:
        return Check("FAIL", "integrated CPN model", "CPN Tools generator version not found")
    return Check("PASS", "integrated CPN model", f"CPN Tools {match.group(1)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat archival release blockers (integrated model and native CPN exports) as failures",
    )
    args = parser.parse_args()
    root = args.repo.resolve()
    checks: list[Check] = []

    core_files = [
        "README.md",
        "CITATION.cff",
        ".zenodo.json",
        "LICENSE",
        "requirements.lock.txt",
        "environment/EXPERIMENTAL_ENVIRONMENT.md",
        "model/scenarios/scenarios.yaml",
        "model/monitors/MONITOR_CATALOGUE.md",
        "results/headline_metrics.json",
        "data/raw/prototype/realtime_api_run_matrix.csv",
        "data/raw/cpn_proxy/Q1_SPoS_MSC_CPN_Output_Matrix_100runs.xlsx",
        "scripts/run_scenarios.py",
        "analysis/summarise_cpn_proxy.py",
        "analysis/summarise_prototype.py",
    ]
    checks.extend(check_file(root, name) for name in core_files)

    integrated = root / "model" / "integrated" / CANONICAL_CPN
    cpn_check = validate_cpn_version(integrated)
    if args.strict and cpn_check.level == "WARN":
        cpn_check.level = "FAIL"
    checks.append(cpn_check)

    native_exports = root / "data" / "raw" / "cpn_native"
    if native_exports.is_dir() and any(path.is_file() and path.name != "README.md" for path in native_exports.iterdir()):
        checks.append(Check("PASS", "native CPN monitor exports", "present"))
    else:
        level = "FAIL" if args.strict else "WARN"
        checks.append(Check(level, "native CPN monitor exports", "not present"))

    try:
        prototype = pd.read_csv(root / "data/raw/prototype/realtime_api_run_matrix.csv")
        checks.append(
            Check("PASS" if len(prototype) == 700 else "FAIL", "prototype rows", str(len(prototype)))
        )
        scenario_counts = prototype.groupby("scenario").size().to_dict()
        expected_counts = {f"Q{i}": 100 for i in range(1, 8)}
        checks.append(
            Check(
                "PASS" if scenario_counts == expected_counts else "FAIL",
                "prototype scenario balance",
                json.dumps(scenario_counts, sort_keys=True),
            )
        )
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("FAIL", "prototype dataset", repr(exc)))
        prototype = None

    try:
        headline = json.loads((root / "results/headline_metrics.json").read_text(encoding="utf-8"))
        if prototype is not None:
            p = headline["prototype_benchmark"]
            totals = {
                "transactions": int(prototype["submitted_tx"].sum()),
                "finality_certificates": int(prototype["finality_certificates"].sum()),
                "receipts": int(prototype["receipts"].sum()),
            }
            for key, actual in totals.items():
                expected = int(p[key])
                checks.append(
                    Check(
                        "PASS" if actual == expected else "FAIL",
                        f"headline prototype {key}",
                        f"dataset={actual}, headline={expected}",
                    )
                )
            finality = 100.0 * totals["finality_certificates"] / totals["transactions"]
            receipt = 100.0 * totals["receipts"] / totals["transactions"]
            checks.append(
                Check(
                    "PASS" if approximate(finality, p["weighted_finality_success_percent"], 0.001) else "FAIL",
                    "headline prototype finality success",
                    f"dataset={finality:.4f}, headline={p['weighted_finality_success_percent']}",
                )
            )
            checks.append(
                Check(
                    "PASS" if approximate(receipt, p["weighted_receipt_success_percent"], 0.001) else "FAIL",
                    "headline prototype receipt success",
                    f"dataset={receipt:.4f}, headline={p['weighted_receipt_success_percent']}",
                )
            )
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("FAIL", "headline metrics", repr(exc)))

    primary_proxy = root / "data/raw/cpn_proxy/SPoS_MSC_Q1_Q7_CPN_Output_Matrices_100runs.xlsx"
    try:
        proxy = pd.read_excel(primary_proxy, sheet_name="AllRuns_OutputMatrix")
        checks.append(Check("PASS" if len(proxy) == 700 else "FAIL", "CPN-proxy rows", str(len(proxy))))
        proxy_counts = proxy.groupby("Scenario").size().to_dict()
        expected_proxy_counts = {f"Q{i}": 100 for i in range(1, 8)}
        checks.append(
            Check(
                "PASS" if proxy_counts == expected_proxy_counts else "FAIL",
                "CPN-proxy scenario balance",
                json.dumps(proxy_counts, sort_keys=True),
            )
        )
        cpn_headline = headline["cpn_proxy"]
        submitted = int(
            proxy["P_MSC2_RoutedShardMempool[Shard1Tx]"].sum()
            + proxy["P_MSC2_RoutedShardMempool[Shard2Tx]"].sum()
        )
        proxy_totals = {
            "transactions": submitted,
            "finality_certificates": int(proxy["P_SP4_FinalityCertificates[Total]"].sum()),
            "receipts": int(proxy["P_MSC3_ReceiptQueue[Total]"].sum()),
        }
        for key, actual in proxy_totals.items():
            expected_value = int(cpn_headline[key])
            checks.append(
                Check(
                    "PASS" if actual == expected_value else "FAIL",
                    f"headline CPN-proxy {key}",
                    f"dataset={actual}, headline={expected_value}",
                )
            )
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("FAIL", "primary CPN-proxy workbook", repr(exc)))

    widths = {"PASS": 4, "WARN": 4, "FAIL": 4}
    print("SPoS-MSC repository validation")
    print("=" * 72)
    for item in checks:
        print(f"[{item.level:<{widths[item.level]}}] {item.name}: {item.detail}")

    failures = [item for item in checks if item.level == "FAIL"]
    warnings = [item for item in checks if item.level == "WARN"]
    print("-" * 72)
    print(f"Checks: {len(checks)} | failures: {len(failures)} | warnings: {len(warnings)}")
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
