# Reference runtime emulator

The manuscript reports a Python/FastAPI single-process reference runtime emulator as a **secondary engineering trend check**. The current source package supplies only the manuscript-level seven-scenario summary in `data/reference_runtime_scenario_summary.csv` and the reported cross-layer correlations.

The emulator source code, environment lock file, and raw 100-run-per-scenario outputs are not present in the materials supplied for repository construction. Therefore, this directory does not claim full emulator reproducibility.

For a provenance-complete release, add:

```text
runtime-emulator/
├── src/
├── tests/
├── requirements.txt or environment.yml
├── data/raw/q1_q7_700_runs.csv
├── scripts/run_q1_q7.py
└── docs/EXECUTION_ENVIRONMENT.md
```

The reported `receipts_per_second` value is an in-memory lifecycle-event processing rate, not public-network blockchain throughput.
