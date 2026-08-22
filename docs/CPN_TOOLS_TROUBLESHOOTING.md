# CPN Tools execution and troubleshooting

## Environment

- CPN Tools 4.0.1
- Use a short ASCII-only Windows path, for example `C:/CPN/SPoS_MSC_v4/`.
- Open only the final v4 model and wait for syntax checking to complete.

## Execution order

1. `CPN_Run_00_Declaration_Check_v4.sml`
2. `CPN_Run_00_Smoke_2_v4.sml`
3. `CPN_Run_01_Sensitivity_Pilot_3_v4.sml`
4. `CPN_Run_02_Default_Configuration_Audit_100_v4.sml`
5. `CPN_Run_03_Sensitivity_OFAT_100_v4.sml`

Load a script with forward slashes:

```sml
use "C:/CPN/SPoS_MSC_v4/CPN_Run_00_Smoke_2_v4.sml";
```

## Common failures

### `unclosed string`

A Windows path written with single backslashes is parsed as SML escape sequences. Use forward slashes or doubled backslashes.

Incorrect:

```sml
ipSetCSVFile("C:\CPN\SPoS_MSC_v4\output.csv");
```

Correct:

```sml
ipSetCSVFile("C:/CPN/SPoS_MSC_v4/output.csv");
```

### One-replication scripted call

Use the supplied two-replication smoke script. For one interactive run, set parameters, apply Rewind, then use Play/Fast Forward rather than calling the replication function with one.

### Empty `P_SensitivityData`

The place has an empty initial marking. Its token appears after scenario-generation fires; it is an output/provenance path rather than an initial control token.
