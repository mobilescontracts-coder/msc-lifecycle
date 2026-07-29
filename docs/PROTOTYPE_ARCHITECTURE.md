# Architecture

The prototype mirrors the integrated SPoS-MSC CPN model.

## CPN-to-prototype mapping

| CPN concept | Prototype module | Function |
|---|---|---|
| Input validators | `scenarios.py` | `generate_validators` |
| Mobile transaction buffer | `scenarios.py` | `generate_transactions` |
| Validator scoring | `spos.py` | `prepare_validators` |
| VRF committee formation | `spos.py` | `form_vrf_committees` |
| Shard routing | `msc.py` | `route_transactions` |
| SPoS finality | `msc.py` | `run_finality` |
| Receipt and reward | `msc.py` | `generate_receipts_rewards` |
| Output metrics | `metrics.py`, `simulation.py` | `gini`, `hhi`, `summarize`, `export_results` |

## Lifecycle sequence

```text
Mobile Tx generation
        ↓
Edge packaging
        ↓
Load-aware shard routing
        ↓
SPoS validator scoring
        ↓
VRF-style committee formation
        ↓
Shard-level finality
        ↓
Receipt generation
        ↓
Reward and evidence export
        ↓
Run matrix / summary Excel
```

## Output matrix fields

The run matrix includes:

- submitted transactions,
- routed transactions,
- finality certificates,
- receipts,
- reward events,
- quarantine events,
- reconfiguration events,
- finality success rate,
- receipt success rate,
- throughput,
- finality latency,
- receipt latency,
- cross-shard ratio,
- shard-load imbalance,
- reward Gini,
- reward HHI,
- owner concentration,
- Nakamoto coefficient.
