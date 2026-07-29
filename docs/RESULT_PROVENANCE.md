# Result Provenance

## CPN-proxy workbooks

The workbooks under `data/raw/cpn_proxy/` contain a README sheet stating that they were produced by a Python emulation of integrated CPN semantics and are not native CPN Tools monitor exports. They are retained because they underpin figures and numerical discussion generated during manuscript development.

## Prototype data

`data/raw/prototype/realtime_api_run_matrix.csv` contains 700 run-level observations from the controlled API benchmark. `realtime_overall_kpis.csv` records aggregate transaction, certificate, receipt, success-rate, and elapsed-time values.

## Processed summaries

Files under `data/processed/` are derivative data used for tables and figures. They must be reproducible from raw files using scripts under `analysis/`.

## Release rule

A journal-linked release must identify, without ambiguity, which manuscript tables and figures use:

- native CPN Tools output;
- CPN-semantics proxy/emulation output;
- prototype simulation output;
- real-time implementation benchmark output.
