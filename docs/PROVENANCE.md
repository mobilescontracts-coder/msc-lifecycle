# Provenance and versioning

## Public model versions

- **v3** is the predecessor self-logging model before sensitivity parameterisation.
- **v4** is the final public sensitivity-enabled model.

The repository intentionally omits intermediate development labels to keep the public artefact sequence clear.

## v4 default-configuration audit

The raw 700-row file retains the execution-time identifier `DEFAULT_EQ`, but the manuscript and repository describe it as a **default-configuration audit**. The v4 matrix reproduces the core v3 lifecycle totals but differs in four stochastic diagnostic totals:

| Metric | Archived v3 aggregate | v4 aggregate | Difference |
|---|---:|---:|---:|
| Cross-shard transactions | 4,995 | 4,987 | −8 |
| Reward events | 94,912 | 94,899 | −13 |
| Reconfiguration events | 1,401 | 1,393 | −8 |
| Integrated evidence records | 316,374 | 316,366 | −8 |

For this reason, v4 is not described as bit-for-bit output-equivalent to v3. The active manuscript uses v4 evidence consistently for both scenario and sensitivity results.

## Missing provenance artefacts

The source package does not include:

- native CPN Tools replication-report folders and simulation-output directories;
- archived v3 raw 700-row matrix;
- runtime-emulator source and raw 100-run-per-scenario outputs.

Their absence is documented in the repository release checklist.
