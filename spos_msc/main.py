"""FastAPI service for the SPoS-MSC prototype."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .scenarios import SCENARIOS
from .simulation import export_results, run_scenarios, run_single_scenario, summarize


class RunRequest(BaseModel):
    scenario_id: Literal["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"] = "Q1"
    runs: int = Field(default=100, ge=1, le=1000)
    seed: int = 626
    export: bool = True


class AllScenarioRunRequest(BaseModel):
    runs: int = Field(default=100, ge=1, le=1000)
    seed: int = 626
    export: bool = True


app = FastAPI(
    title="SPoS-MSC Prototype API",
    version="0.1.0",
    description="Research prototype for the complete MSC lifecycle with scalable SPoS consensus.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "spos-msc-prototype"}


@app.get("/api/v1/scenarios")
def list_scenarios():
    return [scenario.__dict__ for scenario in SCENARIOS.values()]


@app.post("/api/v1/scenarios/run")
def run_scenario(request: RunRequest):
    try:
        df = run_scenarios([request.scenario_id], runs=request.runs, base_seed=request.seed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    summary = summarize(df).to_dict(orient="records")
    response = {"summary": summary, "rows": len(df)}
    if request.export:
        output_dir = Path(os.getenv("SPOS_MSC_OUTPUT_DIR", "outputs"))
        paths = export_results(df, output_dir, prefix=f"{request.scenario_id}_spos_msc")
        response["files"] = {k: str(v) for k, v in paths.items()}
    return response


@app.post("/api/v1/scenarios/run-all")
def run_all_scenarios(request: AllScenarioRunRequest):
    df = run_scenarios(SCENARIOS.keys(), runs=request.runs, base_seed=request.seed)
    summary = summarize(df).to_dict(orient="records")
    response = {"summary": summary, "rows": len(df)}
    if request.export:
        output_dir = Path(os.getenv("SPOS_MSC_OUTPUT_DIR", "outputs"))
        paths = export_results(df, output_dir, prefix="Q1_Q7_spos_msc")
        response["files"] = {k: str(v) for k, v in paths.items()}
    return response


@app.get("/api/v1/scenarios/{scenario_id}/run/{run_id}")
def get_single_run(scenario_id: str, run_id: int, seed: int = 626):
    try:
        output = run_single_scenario(scenario_id, run_id=run_id, seed=seed + run_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return output.as_dict()
