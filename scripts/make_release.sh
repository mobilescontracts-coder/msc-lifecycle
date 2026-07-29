#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python analysis/summarise_cpn_proxy.py
python analysis/summarise_prototype.py
python analysis/generate_figures.py
pytest -q
ruff check spos_msc scripts analysis tests
python scripts/validate_repository.py --strict
python scripts/generate_checksums.py

echo "Release checks passed. Create and push a version tag only after updating"
echo "CITATION.cff, .zenodo.json, CHANGELOG.md, and the manuscript commit record."
