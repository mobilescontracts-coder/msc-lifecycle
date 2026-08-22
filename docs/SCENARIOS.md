# Q1–Q7 scenario design

The seven scenarios are bounded composite stress configurations at a fixed population of four shards and ten input validators. They are not shard-count scale-out experiments or independently implemented protocol baselines.

| Scenario | Name | Tx/run | Committee/quorum | Load threshold | Max logical time | Principal stress |
|---|---|---:|---:|---:|---:|---|
| Q1 | Normal | 24 | 3/2 | 75 | 180 | Nominal end-to-end lifecycle |
| Q2 | High load | 40 | 3/2 | 75 | 180 | Offered-load pressure and bounded pre-finality failure injection |
| Q3 | Cross-shard | 28 | 3/2 | 75 | 180 | Cross-contract/cross-shard dependencies |
| Q4 | Poor connectivity | 24 | 3/2 | 75 | 240 | Admission degradation and receipt-delivery timeout |
| Q5 | Stake skew | 24 | 3/2 | 75 | 180 | Shared ownership with concentrated high stake |
| Q6 | Risky/offline | 24 | 4/3 | 75 | 180 | Risk exclusion, quarantine, and committee recovery |
| Q7 | Hot shard | 32 | 3/2 | 55 | 180 | Hotspot pressure and adaptive reconfiguration |

The machine-readable version is `experiments/cpn-tools/scenario_matrix.csv`.
