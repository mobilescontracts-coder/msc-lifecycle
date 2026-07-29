# Research Mapping for the Paper

## Role in the research programme

- MSC paper: mobile-aware lifecycle, shard routing, receipt protocol, CPN, ISSRM.
- SPoS paper: owner-aware mobile-friendly PoS, VRF committee, rewards, slashing, decentralization metrics.
- SPoS-MSC prototype: integrated lifecycle + SPoS consensus + output matrix generation.

## How to describe in the manuscript

> The prototype implements a Python/FastAPI research emulator of the integrated SPoS-MSC model. It is used to execute the Q1-Q7 Qtum-inspired scenarios and export run-level output matrices corresponding to the CPN output places. The prototype does not replace the formal CPN model; rather, it provides a reproducible software artifact for exploring the integrated lifecycle and generating experimental evidence.

## CPN output places represented by the prototype

| Integrated CPN output | Prototype field |
|---|---|
| `P_MSC2_RoutedShardMempool` | `routed_tx` |
| `P_SP4_FinalityCertificates` | `finality_certificates` |
| `P_MSC3_ReceiptQueue` | `receipts` |
| `P_SP5_RewardEvents` | `reward_events`, `total_reward` |
| `P_SP6_ShardLoad` | `shard1_load`, `shard2_load`, `shard_load_std` |
| `P_SP8_ReconfigurationEvents` | `reconfiguration_events` |
| `P_SP9_QuarantineAndSlashingLog` | `quarantine_events` |
| `P_SP10_IntegratedEvidenceLog` | `evidence_events` |

## Suggested claims

Safe claim:

> The prototype demonstrates that the integrated SPoS-MSC logic can be executed as a reproducible software artifact and can generate run-level matrices for performance, scalability, validator, and decentralization analysis.

Avoid claiming:

> The prototype outperforms production Qtum or production sharded blockchains.

Unless a real network implementation and identical benchmark conditions are provided.
