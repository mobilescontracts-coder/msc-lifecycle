# Analysis pipeline

`analyze_spos_msc_v4.py` validates the four native CPN matrices, calculates derived run-level metrics, produces Q1–Q7 descriptive statistics, performs the three-level local sensitivity analysis, and regenerates the manuscript figures.

Run from the repository root:

```bash
scripts/run_analysis.sh
```

Reference CSV outputs appear in `analysis/reference_outputs/`; newly generated outputs appear in `analysis/reproduced/` and are ignored by Git.

`compare_spos_msc_predecessor_audit.py` supports comparison with an archived v3 raw matrix when that matrix becomes available.
