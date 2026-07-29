# Analysis scripts

The scripts in this directory rebuild scenario summaries and figures from the
committed raw datasets.

```bash
python analysis/summarise_cpn_proxy.py
python analysis/summarise_prototype.py
python analysis/generate_figures.py
```

Outputs are written to `outputs/reproduced/`.

## Evidence labels

- `summarise_cpn_proxy.py` processes workbooks that explicitly identify
  themselves as a Python proxy/emulation of the integrated CPN semantics.
  They are **not native CPN Tools monitor exports**.
- `summarise_prototype.py` processes run-level measurements produced by the
  tested Python prototype and its local API benchmark.
- Native CPN monitor exports, when available, must be stored separately under
  `data/raw/cpn_native/` and analysed with a dedicated, provenance-preserving
  script.
