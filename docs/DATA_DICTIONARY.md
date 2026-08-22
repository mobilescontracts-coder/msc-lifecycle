# CPN CSV data dictionary

All four supplied native CSV matrices share the same schema. Derived metrics are computed by `analysis/analyze_spos_msc_v4.py`.

| Column | Type | Unit/role | Description |
|---|---|---|---|
| `experiment_id` | string | identifier | Experiment family identifier, such as SMOKE, PILOT, DEFAULT_EQ, or OFAT. |
| `factor_id` | string | identifier | Sensitivity factor identifier or scenario-design identifier. |
| `level_id` | string | identifier | Sensitivity level: LOW, DEFAULT, HIGH, or a default audit label. |
| `configuration` | string | provenance | Pipe-delimited resolved executable parameter vector used for the run. |
| `scenario_id` | integer | identifier | Q1–Q7 scenario number encoded as 1–7. |
| `run_id` | integer | identifier | Run identifier within the factor/level or scenario cell. |
| `base_seed` | integer | provenance | Model-level base seed; 626 in the supplied matrices. |
| `model_time` | integer | logical time | Logical CPN model time when the run finalises. |
| `stop_code` | string | status | Explicit terminal status; COMPLETE for all validated rows. |
| `submitted_tx` | integer | count | Submitted mobile transactions in the run. |
| `prepared_tx` | integer | count | Transactions that pass preparation/admission. |
| `routed_tx` | integer | count | Prepared transactions routed to a shard. |
| `cross_shard_tx` | integer | count | Submitted transactions classified as cross-shard. |
| `shard_blocks` | integer | count | Shard blocks produced. |
| `eligible_validators` | integer | count | Validators satisfying the active eligibility policy. |
| `active_committees` | integer | count | Active shard committees recorded in the run. |
| `committee_recoveries` | integer | count | Abstract committee-completion/recovery events. |
| `finality_certificates` | integer | count | Transactions receiving a finality certificate. |
| `root_commitments` | integer | count | Transactions receiving a root-chain commitment. |
| `receipts` | integer | count | Mobile receipts delivered successfully. |
| `terminal_failures` | integer | count | Explicit terminal failures; receipts + failures = submitted. |
| `reward_events` | integer | count | Recorded proposer, voter, and receipt reward events. |
| `quarantine_events` | integer | count | Validator quarantine events. |
| `slashing_events` | integer | count | Validator slashing/penalty events. |
| `reconfiguration_events` | integer | count | Adaptive shard reconfiguration events. |
| `evidence_count` | integer | count | Integrated lifecycle/governance evidence records. |
| `finality_latency_sum` | integer | logical time | Sum of finality latencies for observed finality events. |
| `finality_latency_n` | integer | count | Number of observations in finality_latency_sum. |
| `receipt_latency_sum` | integer | logical time | Sum of receipt latencies for observed receipt events. |
| `receipt_latency_n` | integer | count | Number of observations in receipt_latency_sum. |
| `reward_gini_bp` | integer | scaled metric | Reward Gini scaled by 100; divide by 100 for the reported 0–100 value. |
| `reward_hhi_bp` | integer | scaled metric | Reward HHI scaled by 100; divide by 100 for the reported 0–100 value. |
| `nakamoto_coefficient` | integer | count | Reward-based 51% concentration coefficient recorded by the model. |
| `owner_concentration_bp` | integer | scaled metric | Largest-owner reward share scaled by 100; divide by 100 for percent. |
| `shard_load_std_bp` | integer | scaled metric | Shard-load standard deviation scaled by 100; divide by 100. |
