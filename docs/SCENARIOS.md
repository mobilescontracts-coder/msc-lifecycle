# Q1–Q7 scenario catalogue

The manuscript uses seven scenario families. Each reported scenario contains
100 run-level observations in both the CPN-proxy and prototype datasets.

| ID | Scenario | Primary stressor | Principal metrics |
|---|---|---|---|
| Q1 | Normal mobile contract request | Nominal balanced operation | Finality, receipts, latency |
| Q2 | High-load mobile dApp | Increased transaction demand | Throughput, load, reconfiguration |
| Q3 | Cross-contract/cross-shard request | Cross-shard dependencies | Cross-shard ratio, receipt latency |
| Q4 | Poor mobile connectivity | Degraded mobile/edge path | Receipt success, latency, quarantine |
| Q5 | Stake-skewed validator set | Disproportionate owner/validator stake | Gini, HHI, owner concentration |
| Q6 | Risky/offline validator case | Unsafe or unavailable validators | Quarantine, recovery, finality |
| Q7 | Hot-shard workload | Concentrated shard demand | Load imbalance, reconfiguration, receipts |

The machine-readable scenario definition is in
[`model/scenarios/scenarios.yaml`](../model/scenarios/scenarios.yaml). Any
change to a scenario must be versioned and must state whether earlier results
remain comparable.
