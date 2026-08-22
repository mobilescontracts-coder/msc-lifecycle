# Local sensitivity design

The main parameter study uses a three-level one-factor-at-a-time design:

\[
8\ \text{factors}\times3\ \text{levels}\times100\ \text{replications}=2{,}400\ \text{runs}.
\]

| Factor | Anchor | Low | Default | High | Primary response |
|---|---|---:|---:|---:|---|
| Transactions per run | Q1 | 16 | 24 | 40 | Logical throughput |
| Forced cross-shard demand | Q3 | 20% | 60% | 80% | Receipt latency |
| Request disconnection | Q4 | 10% | 20% | 30% | Finality success |
| Receipt delivery drop | Q4 | 10% | 29% | 40% | Receipt success |
| Owner-stake cap | Q5 | 1500 | 3000 | 6000 | Largest-owner reward share |
| Mobile-fitness threshold | Q6 | 25 | 35 | 65 | Eligible validators |
| Committee-size/quorum policy | Q6 | 3/2 | 4/3 | 5/4 | Committee recovery |
| Reconfiguration load threshold | Q7 | 45 | 55 | 75 | Reconfiguration events |

The committee-size/quorum entry is a categorical policy factor because both values change together.

The study is **local** to the selected levels. It does not estimate Sobol indices, Morris effects, global variance decomposition, or higher-order interactions.
