#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/verify_checksums.sh"
python -m pytest -q "$ROOT/tests"
"$ROOT/scripts/run_analysis.sh"
python "$ROOT/analysis/verify_reference_outputs.py" \
  --generated "$ROOT/analysis/reproduced" \
  --reference "$ROOT/analysis/reference_outputs"
"$ROOT/scripts/build_manuscript.sh"
