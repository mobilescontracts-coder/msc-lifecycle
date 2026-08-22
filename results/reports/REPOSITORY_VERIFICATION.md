# Repository verification

Verification date: 2026-08-18

## Automated tests

```text
9 passed
```

The tests cover:

- row counts and factor/scenario cell cardinality;
- explicit `COMPLETE` stop codes;
- base seed logging;
- run-ID coverage;
- duplicate-key detection;
- lifecycle-ordering invariants;
- terminal accounting;
- v4 aggregate totals;
- primary sensitivity reference values;
- data dictionary and datapackage coverage;
- public v3 → v4 manuscript version sequence.

## Analysis reproduction

The complete analysis pipeline reproduces the following archived CSV outputs exactly:

- `Validation_Summary.csv`
- `v4_Default_Scenario_Statistics.csv`
- `v4_Sensitivity_Descriptive_Statistics.csv`
- `v4_Sensitivity_Primary_Responses.csv`
- `v4_Sensitivity_Independent_Contrasts.csv`

## Manuscript build

- Build tool: `latexmk -pdf` with BibTeX
- Pages: 32
- Fatal errors: 0
- Undefined citations: 0
- Undefined references: 0
- Overfull boxes: 1 (Elsevier CAS front matter)
- Underfull boxes: 67 (primarily dense tables)
- PDF author metadata: `Vipin Deval; Vimal Dwivedi; Alex Norta; Dirk Draheim`
- Deterministic PDF SHA-256: `fe07fbfd105423b4211a3ab1865edd38ef428b056afd86b1c7ca2c4f556db9aa`
- Fixed `SOURCE_DATE_EPOCH`: `1787011200`

## Native-execution limitation

The CPN Tools GUI cannot be executed in the repository CI. Native replay requires CPN Tools 4.0.1 on Windows. The repository validates the supplied native CSV matrices and preserves the scripts required for rerunning them.
