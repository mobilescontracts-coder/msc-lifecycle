#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python "$ROOT/analysis/analyze_spos_msc_v4.py" \
  --smoke-csv "$ROOT/data/raw/cpn/SPoS_MSC_v4_smoke_2.csv" \
  --pilot-csv "$ROOT/data/raw/cpn/SPoS_MSC_v4_sensitivity_pilot_72.csv" \
  --default-csv "$ROOT/data/raw/cpn/SPoS_MSC_v4_default_configuration_audit_700.csv" \
  --ofat-csv "$ROOT/data/raw/cpn/SPoS_MSC_v4_sensitivity_OFAT_2400.csv" \
  --output-dir "$ROOT/analysis/reproduced"
