from spos_msc.simulation import run_scenarios, run_single_scenario


def test_q1_single_run_produces_output():
    out = run_single_scenario("Q1", run_id=1, seed=626)
    assert out.submitted_tx > 0
    assert out.routed_tx == out.submitted_tx
    assert out.finality_certificates <= out.routed_tx
    assert out.receipts <= out.finality_certificates
    assert out.reward_events >= out.receipts


def test_all_scenarios_small_run_matrix():
    df = run_scenarios(["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"], runs=2, base_seed=626)
    assert len(df) == 14
    assert set(df["scenario"]) == {"Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"}
    assert (df["submitted_tx"] > 0).all()
