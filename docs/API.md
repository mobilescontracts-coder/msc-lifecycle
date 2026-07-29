# API Documentation

Run locally:

```bash
uvicorn spos_msc.main:app --host 0.0.0.0 --port 8000
```

Interactive API docs:

```text
http://localhost:8000/docs
```

## Run one scenario

```bash
curl -X POST http://localhost:8000/api/v1/scenarios/run \
  -H 'Content-Type: application/json' \
  -d '{"scenario_id":"Q5", "runs":100, "seed":626, "export":true}'
```

## Run all scenarios

```bash
curl -X POST http://localhost:8000/api/v1/scenarios/run-all \
  -H 'Content-Type: application/json' \
  -d '{"runs":100, "seed":626, "export":true}'
```

## Inspect one run

```bash
curl "http://localhost:8000/api/v1/scenarios/Q1/run/1?seed=626"
```
