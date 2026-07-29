#!/usr/bin/env python3
"""Run Q1--Q7 SPoS-MSC scenario experiments and export matrices.

Example:
    python scripts/run_scenarios.py --runs 100 --output outputs
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spos_msc.scenarios import SCENARIOS
from spos_msc.simulation import export_results, run_scenarios


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=100, help="Runs per scenario")
    parser.add_argument("--seed", type=int, default=626, help="Base random seed")
    parser.add_argument("--output", type=Path, default=Path("outputs"), help="Output directory")
    parser.add_argument(
        "--scenarios",
        nargs="*",
        default=list(SCENARIOS.keys()),
        help="Scenario IDs, e.g., Q1 Q2 Q7. Defaults to Q1--Q7.",
    )
    args = parser.parse_args()
    df = run_scenarios(args.scenarios, runs=args.runs, base_seed=args.seed)
    paths = export_results(df, args.output, prefix="Q1_Q7_spos_msc")
    print(f"Generated {len(df)} run rows")
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
