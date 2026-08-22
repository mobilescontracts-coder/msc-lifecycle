#!/usr/bin/env python3
"""Compare regenerated analysis CSVs with the archived reference outputs."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

FILES = [
    "Validation_Summary.csv",
    "v4_Default_Scenario_Statistics.csv",
    "v4_Sensitivity_Descriptive_Statistics.csv",
    "v4_Sensitivity_Primary_Responses.csv",
    "v4_Sensitivity_Independent_Contrasts.csv",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    args = parser.parse_args()

    for name in FILES:
        generated = pd.read_csv(args.generated / name)
        reference = pd.read_csv(args.reference / name)
        assert_frame_equal(generated, reference, check_dtype=False, rtol=1e-12, atol=1e-12)
        print(f"PASS: {name}")


if __name__ == "__main__":
    main()
