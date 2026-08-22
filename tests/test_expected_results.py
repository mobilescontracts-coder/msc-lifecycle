from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "cpn"
REF = ROOT / "analysis" / "reference_outputs"


def test_v4_default_aggregate_totals():
    frame = pd.read_csv(RAW / "SPoS_MSC_v4_default_configuration_audit_700.csv")
    expected = {
        "submitted_tx": 19600,
        "prepared_tx": 18941,
        "routed_tx": 18941,
        "cross_shard_tx": 4987,
        "shard_blocks": 18767,
        "finality_certificates": 18767,
        "root_commitments": 18767,
        "receipts": 18187,
        "terminal_failures": 1413,
        "reward_events": 94899,
        "committee_recoveries": 115,
        "quarantine_events": 200,
        "slashing_events": 200,
        "reconfiguration_events": 1393,
        "evidence_count": 316366,
    }
    for column, value in expected.items():
        assert int(frame[column].sum()) == value

    finality = 100 * frame["finality_certificates"].sum() / frame["submitted_tx"].sum()
    receipt = 100 * frame["receipts"].sum() / frame["submitted_tx"].sum()
    assert np.isclose(finality, 95.75, atol=0.005)
    assert np.isclose(receipt, 92.7908163265, atol=1e-10)


def test_primary_sensitivity_reference_values():
    primary = pd.read_csv(REF / "v4_Sensitivity_Primary_Responses.csv").set_index("factor_id")
    expected = {
        "WORKLOAD": (0.33433997690641526, 0.445436751854336, 0.6806162457579539, 0.8983550993074023),
        "CROSS_SHARD_PCT": (37.36392857142857, 43.984642857142845, 47.293571428571425, 0.8893577576660023),
        "REQUEST_OFFLINE_PCT": (81.75, 72.54166666666667, 63.29166666666667, 0.8357970644076351),
        "RECEIPT_DROP_PCT": (63.875, 48.375, 39.833333333333336, 0.8407543165170702),
        "OWNER_CAP": (33.0523, 45.5559, 38.9596, 0.19204705942149822),
        "MOBILE_THRESHOLD": (6.0, 6.0, 3.0, 1.0),
        "COMMITTEE_QUORUM": (0.48, 1.15, 2.25, 0.6299069921968901),
        "LOAD_THRESHOLD": (10.17, 7.86, 4.15, 0.8629421019936484),
    }
    for factor, values in expected.items():
        actual = primary.loc[factor, ["low_mean", "default_mean", "high_mean", "epsilon_squared"]].to_numpy(float)
        assert np.allclose(actual, values, rtol=1e-12, atol=1e-12)


def test_manuscript_and_public_model_use_v4_sequence():
    manuscript = (ROOT / "manuscript" / "Manuscript_SMPT.tex").read_text(encoding="utf-8")
    assert "public v4" in manuscript
    assert "2,400" in manuscript
    assert "SPoS_MSC_Hierarchical_Executable_v4_Sensitivity" in manuscript
    assert "public v8" not in manuscript
