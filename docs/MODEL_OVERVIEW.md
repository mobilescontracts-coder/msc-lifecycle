# Model overview

SPoS-MSC is a hierarchical timed Coloured Petri Net that connects a mobile smart-contract lifecycle with incentive-aware Proof-of-Stake governance.

## Final public v4 structure

| Element | Count |
|---|---:|
| Pages | 13 |
| Places | 171 |
| Transitions | 40 |
| Arcs | 380 |
| Hierarchy instances | 13 |
| Colour sets | 58 |

## Execution domains

- **D1 — Mobile access and preparation:** scenario initialisation, mobile request admission, edge/request preparation, and sensitivity provenance.
- **D2 — Sharded execution:** adaptive routing, load monitoring, reconfiguration, contract execution, block/proof evidence.
- **D3 — Validator governance and finality:** owner-aware scoring, eligibility, committee formation/recovery, voting, quorum certificates.
- **D4 — Commitment, receipts, incentives, and termination:** root commitment, mobile receipt handling, rewards/penalties, concentration metrics, run summary, explicit completion.

## Functional stages

| Stage | Function |
|---|---|
| ST_01 | Prepare mobile request and execution context |
| ST_02 | Route to a shard and expose load/reconfiguration evidence |
| ST_03 | Score validators using ownership, stake, mobile suitability and risk |
| ST_04 | Form or recover committees |
| ST_05 | Execute shard block and generate proof evidence |
| ST_06 | Reach committee-controlled finality |
| ST_07 | Create root commitment and mobile receipt outcome |
| ST_08 | Apply rewards/penalties, compute decentralisation metrics, and terminate |

## Sensitivity provenance

The v4 model defines `IP_SENSITIVITY` and exposes a hierarchy-connected `P_SensitivityData` path from ST_01 through D1 to the top page. The token records experiment, factor, level, scenario, run, and the resolved configuration string. Every self-logged CSV row contains the same configuration provenance.

## Model files

- `models/v3-predecessor/` contains the predecessor self-logging model.
- `models/v4-sensitivity/` contains the final public model used for the supplied v4 data.
- `models/aom/` contains the editable three-page AOM goal-model source.
