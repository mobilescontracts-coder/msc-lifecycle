#!/usr/bin/env bash
set -euo pipefail
BASE_URL=${BASE_URL:-http://localhost:8000}

echo "Health check"
curl -s "$BASE_URL/health" | python -m json.tool

echo "List scenarios"
curl -s "$BASE_URL/api/v1/scenarios" | python -m json.tool

echo "Run Q1 with 5 runs"
curl -s -X POST "$BASE_URL/api/v1/scenarios/run" \
  -H 'Content-Type: application/json' \
  -d '{"scenario_id":"Q1", "runs":5, "seed":626, "export":false}' | python -m json.tool
