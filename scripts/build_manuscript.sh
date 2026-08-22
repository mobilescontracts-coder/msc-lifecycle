#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/manuscript"
export SOURCE_DATE_EPOCH=1787011200
latexmk -pdf Manuscript_SMPT.tex
