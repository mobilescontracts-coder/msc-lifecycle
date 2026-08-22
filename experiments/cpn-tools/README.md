# Native CPN Tools experiments

## Required software

CPN Tools 4.0.1 on Windows.

## Files

- `scripts/CPN_Run_00_Declaration_Check_v4.sml`
- `scripts/CPN_Run_00_Smoke_2_v4.sml`
- `scripts/CPN_Run_01_Sensitivity_Pilot_3_v4.sml`
- `scripts/CPN_Run_02_Default_Configuration_Audit_100_v4.sml`
- `scripts/CPN_Run_03_Sensitivity_OFAT_100_v4.sml`

## Model

`../../models/v4-sensitivity/SPoS_MSC_Hierarchical_Executable_v4_Sensitivity.cpn`

## Expected outputs

| Script | Expected rows | Purpose |
|---|---:|---|
| Smoke | 2 | Executable completion gate |
| Pilot | 72 | Parameter logging and cell coverage |
| Default audit | 700 | Q1–Q7 scenario evidence |
| OFAT | 2,400 | Local sensitivity evidence |

See `docs/CPN_TOOLS_TROUBLESHOOTING.md` before execution.
