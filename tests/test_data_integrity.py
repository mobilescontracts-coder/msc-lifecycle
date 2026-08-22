from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "cpn"

CASES = [
    ("SPoS_MSC_v4_smoke_2.csv", 2, ["experiment_id", "factor_id", "level_id"], 1, 2),
    ("SPoS_MSC_v4_sensitivity_pilot_72.csv", 72, ["factor_id", "level_id"], 24, 3),
    ("SPoS_MSC_v4_default_configuration_audit_700.csv", 700, ["scenario_id"], 7, 100),
    ("SPoS_MSC_v4_sensitivity_OFAT_2400.csv", 2400, ["factor_id", "level_id"], 24, 100),
]


@pytest.mark.parametrize("filename,expected_rows,group_cols,expected_groups,per_group", CASES)
def test_native_csv_integrity(filename, expected_rows, group_cols, expected_groups, per_group):
    frame = pd.read_csv(RAW / filename)
    assert len(frame) == expected_rows
    assert set(frame["stop_code"]) == {"COMPLETE"}
    assert set(frame["base_seed"]) == {626}

    groups = frame.groupby(group_cols, dropna=False)
    assert groups.ngroups == expected_groups
    for _, group in groups:
        assert len(group) == per_group
        assert sorted(group["run_id"].astype(int).tolist()) == list(range(1, per_group + 1))

    key_cols = group_cols + ["run_id"]
    assert not frame.duplicated(key_cols).any()

    ordering = (
        (frame["receipts"] <= frame["root_commitments"])
        & (frame["root_commitments"] <= frame["finality_certificates"])
        & (frame["finality_certificates"] <= frame["shard_blocks"])
        & (frame["shard_blocks"] <= frame["routed_tx"])
        & (frame["routed_tx"] <= frame["prepared_tx"])
        & (frame["prepared_tx"] <= frame["submitted_tx"])
    )
    assert ordering.all()
    assert (frame["receipts"] + frame["terminal_failures"] == frame["submitted_tx"]).all()
