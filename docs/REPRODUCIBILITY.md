# Reproducibility protocol

## A. Verify the archived artefacts

```bash
sha256sum --check CHECKSUMS.sha256
```

## B. Reproduce analysis from the supplied native CSV matrices

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python analysis/analyze_spos_msc_v4.py \
  --smoke-csv data/raw/cpn/SPoS_MSC_v4_smoke_2.csv \
  --pilot-csv data/raw/cpn/SPoS_MSC_v4_sensitivity_pilot_72.csv \
  --default-csv data/raw/cpn/SPoS_MSC_v4_default_configuration_audit_700.csv \
  --ofat-csv data/raw/cpn/SPoS_MSC_v4_sensitivity_OFAT_2400.csv \
  --output-dir analysis/reproduced
pytest -q
```

Expected validation:

- 2 smoke rows;
- 72 pilot rows;
- 700 default-scenario rows;
- 2,400 OFAT rows;
- `stop_code=COMPLETE` for every row;
- no duplicate configuration/run keys;
- no ordering or terminal-accounting violations.

## C. Re-run CPN Tools experiments

1. Copy the v4 CPN and all SML scripts to one short Windows path.
2. Open the CPN in CPN Tools 4.0.1 and wait for complete syntax checking.
3. Execute the scripts in numerical order.
4. Preserve generated CSVs, replication reports, and simulation-output directories.
5. Compare new CSV hashes and statistical outputs with the archived release.

## D. Build the manuscript

```bash
cd manuscript
SOURCE_DATE_EPOCH=1787011200 latexmk -pdf Manuscript_SMPT.tex
```

or:

```bash
pdflatex Manuscript_SMPT.tex
bibtex Manuscript_SMPT
pdflatex Manuscript_SMPT.tex
pdflatex Manuscript_SMPT.tex
```

## E. Full-provenance release additions

Before creating an archival DOI, add the native CPN Tools replication folders and the runtime-emulator source/raw outputs described in `docs/RELEASE_CHECKLIST.md`.
