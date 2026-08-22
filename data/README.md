# Data

## Raw CPN matrices

- `SPoS_MSC_v4_smoke_2.csv`
- `SPoS_MSC_v4_sensitivity_pilot_72.csv`
- `SPoS_MSC_v4_default_configuration_audit_700.csv`
- `SPoS_MSC_v4_sensitivity_OFAT_2400.csv`

All rows represent complete native CPN replications. The raw 700-row file retains the execution identifier `DEFAULT_EQ`; the public description is “default-configuration audit.”

## Processed/reference outputs

`data/processed/` and `analysis/reference_outputs/` contain supplied validation and statistical summaries. The analysis script regenerates the principal outputs directly from the raw CSVs.

## Schema

- `schema/data_dictionary.csv`
- `schema/datapackage.json`
- `docs/DATA_DICTIONARY.md`
