# SPoS-MSC

**Executable modelling of a sharded mobile smart-contract lifecycle with incentive-aware Proof-of-Stake governance**

This repository contains the reproducibility artefacts for the SPoS-MSC study: the hierarchical Coloured Petri Net (CPN), native CPN Tools execution scripts, raw scenario and sensitivity matrices, independent statistical-analysis code, manuscript sources, generated figures/tables, and machine-readable provenance metadata.

Repository target: `https://github.com/mobilescontracts-coder/spos-msc`

## Evidence included

| Evidence layer | Artefact | Status |
|---|---|---|
| Executable formal model | Public v4 hierarchical CPN | Included |
| Predecessor provenance | Public v3 self-logging CPN | Included |
| Smoke validation | 2 native CPN replications | Included |
| Parameter-logging pilot | 72 native CPN replications | Included |
| Q1–Q7 scenario experiment | 700 native CPN replications | Included |
| Local OFAT sensitivity | 2,400 native CPN replications | Included |
| Statistical analysis | Validation, descriptive statistics, omnibus tests, contrasts, figures | Included and executable |
| Manuscript | Complete Elsevier CAS LaTeX project and compiled PDF | Included |
| Runtime-emulator summary | Seven scenario means and reported correlations | Included |
| Runtime-emulator source/raw runs | Python/FastAPI source and 700 raw runtime rows | **Not supplied** |
| Native CPN replication folders | CPN Tools report/output directories | **Not supplied** |

The repository is therefore reproducible at the **native CPN CSV, statistical-analysis, figure, table, and manuscript-build levels**. The two missing provenance components are documented rather than fabricated. See [docs/REPRODUCIBILITY_STATUS.md](docs/REPRODUCIBILITY_STATUS.md).

## Public artefact sequence

- **v3** — predecessor self-logging executable before sensitivity parameterisation.
- **v4** — final sensitivity-enabled executable used for the reported 700-run scenario matrix and 2,400-run local OFAT matrix.

Intermediate development snapshots are not public manuscript versions.

## Quick start

### 1. Clone and verify

```bash
git clone https://github.com/mobilescontracts-coder/spos-msc.git
cd spos-msc
sha256sum --check CHECKSUMS.sha256
```

### 2. Reproduce the statistical analysis

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements-lock.txt

python analysis/analyze_spos_msc_v4.py \
  --smoke-csv data/raw/cpn/SPoS_MSC_v4_smoke_2.csv \
  --pilot-csv data/raw/cpn/SPoS_MSC_v4_sensitivity_pilot_72.csv \
  --default-csv data/raw/cpn/SPoS_MSC_v4_default_configuration_audit_700.csv \
  --ofat-csv data/raw/cpn/SPoS_MSC_v4_sensitivity_OFAT_2400.csv \
  --output-dir analysis/reproduced

pytest -q
```

Expected terminal message:

```text
PASS: native matrices satisfy the configured integrity checks.
```

### 3. Build the manuscript

```bash
cd manuscript
SOURCE_DATE_EPOCH=1787011200 latexmk -pdf Manuscript_SMPT.tex
```

The repository also provides `make analysis`, `make test`, `make manuscript`, and `make verify` targets.

### 4. Re-run the native CPN experiments

Native execution requires **CPN Tools 4.0.1**. Open:

```text
models/v4-sensitivity/SPoS_MSC_Hierarchical_Executable_v4_Sensitivity.cpn
```

Then execute the CPN ML scripts in `experiments/cpn-tools/scripts/` in numerical order. See [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) and [docs/CPN_TOOLS_TROUBLESHOOTING.md](docs/CPN_TOOLS_TROUBLESHOOTING.md).

## Repository map

```text
spos-msc/
├── analysis/                  Python validation and statistical analysis
├── data/                      Raw CPN matrices, processed outputs, schemas
├── docs/                      Reproducibility, provenance, design and limits
├── experiments/cpn-tools/     Native CPN ML execution scripts
├── manuscript/                Overleaf-ready Elsevier CAS project
├── models/                    Public v3/v4 CPNs and editable AOM source
├── results/                   Reference figures, tables and reports
├── runtime-emulator/          Supplied manuscript-level runtime summaries
├── tests/                     Automated integrity and regression tests
└── metadata/                  Citation and research-object metadata
```

## Main empirical design

- Q1–Q7 scenario matrix: **7 × 100 = 700** native replications.
- Local OFAT matrix: **8 factors × 3 levels × 100 = 2,400** native replications.
- Base seed logged in all supplied matrices: **626**.
- Statistical unit: one complete CPN replication.
- Low/default/high cells are analysed as separately executed groups; run IDs are provenance identifiers rather than matched statistical pairs.

## Claim boundaries

The artefacts support bounded four-shard scenario behaviour and local three-level sensitivity. They do **not** establish public-network TPS, shard-count scale-out, global sensitivity indices, exhaustive state-space verification, production cryptographic correctness, or causal superiority over unexecuted baselines. See [docs/CLAIM_BOUNDARIES.md](docs/CLAIM_BOUNDARIES.md).

## Citation

Use the repository citation generated from [`CITATION.cff`](CITATION.cff) and cite the associated manuscript when published. Publication/push instructions appear in [docs/GITHUB_PUBLISHING.md](docs/GITHUB_PUBLISHING.md).

## Licence

A public reuse licence requires author approval before release. See [`LICENSE`](LICENSE) and [`docs/LICENSING.md`](docs/LICENSING.md). Third-party Elsevier template files retain their own terms.
