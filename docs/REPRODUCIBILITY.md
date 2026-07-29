# Reproducibility Guide

## 1. Verify the repository

```bash
python scripts/validate_repository.py
```

The validator checks required files, row counts for CSV outputs, CPN Tools generator metadata for included component models, and headline result consistency.

## 2. Run the prototype

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python scripts/run_scenarios.py --runs 100 --seed 626 --output outputs
```

## 3. Run the API benchmark

```bash
uvicorn spos_msc.main:app --host 127.0.0.1 --port 8000
```

Use a separate terminal or benchmark script to issue scenario requests. Record system load, warm-up policy, request order, start/end UTC timestamps, and raw response logs.

## 4. Run the CPN model

See `docs/CPN_EXECUTION.md`. The exact integrated model and native monitor exports are mandatory for a release that claims native CPN Tools execution.

## 5. Recompute summaries

```bash
python analysis/summarise_cpn_proxy.py
python analysis/summarise_prototype.py
python analysis/generate_figures.py
```

## 6. Record the submission commit

```bash
git rev-parse HEAD > SUBMISSION_COMMIT.txt
```

Do this only after all paper-linked files are final and committed.
