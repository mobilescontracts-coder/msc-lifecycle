# Native CPN Tools replication reports

The supplied project contains the executable CPN models, CPN ML run scripts, and the four native CSV matrices, but it does **not** contain the CPN Tools replication-report folders or simulation-output directories generated on the execution workstation.

For a provenance-complete archival release, copy the native CPN Tools reports here using this structure:

```text
native-replication-reports/
├── smoke-2/
├── pilot-72/
├── default-configuration-audit-700/
└── sensitivity-ofat-2400/
```

Do not fabricate or regenerate these folders outside CPN Tools. Their purpose is to substantiate native execution provenance beyond the CSV matrices.
