# CPN Tools execution and export protocol

## Required software

- CPN Tools 4.0.1
- The exact integrated model:
  `model/integrated/SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn`

The component models in `model/components/` are preserved for design
traceability, but they are not substitutes for the integrated benchmark model.

## Import the manuscript-linked model

```bash
python scripts/import_integrated_cpn.py \
  /path/to/SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn
```

The helper validates the CPN XML header, copies the model to its canonical
location, and writes a SHA-256 provenance record.

## Generate one five-policy benchmark block

The integrated benchmark supports these policy modes:

| Mode | Policy |
|---:|---|
| 10 | MSC native / no SPoS governance |
| 20 | Traditional stake-proportional PoS |
| 30 | Round-Robin |
| 40 | Random committee |
| 50 | Full SPoS-MSC |

Patch a model for one scenario/seed block:

```bash
python scripts/make_cpn_benchmark_block.py \
  --base model/integrated/SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn \
  --out outputs/Q6_seed626.cpn \
  --scenario 6 \
  --seed 626 \
  --expected-tx 50 \
  --ablation 0
```

## Native execution procedure

For every scenario and run:

1. Open the patched model in CPN Tools 4.0.1.
2. Run syntax, type, and hierarchy checks.
3. Record the model SHA-256, scenario, run, seed, policy, ablation, and CPN
   Tools version.
4. Execute until all configured runs complete or the declared timeout fires.
5. Export the final result archive and all manuscript-linked monitors without
   manual editing.
6. Store exports under `data/raw/cpn_native/`.
7. Rewind or reopen the model before the next independent block.

## Minimum native monitor fields

Each exported row should identify:

- scenario and run;
- random seed and epoch;
- policy and ablation code;
- submitted and routed transactions;
- active validators and committees;
- finality certificates and root/anchor evidence;
- receipts and reward events;
- quarantine, slashing, recovery, and reconfiguration events;
- finality and receipt latency;
- cross-shard activity and shard-load imbalance;
- Gini, HHI, Nakamoto coefficient, and owner concentration.

## Provenance rule

The workbooks under `data/raw/cpn_proxy/` are model-faithful proxy/emulation
outputs. They may be used for development and independent semantic checking,
but must not be described as native CPN Tools monitor exports. A final archival
release should preserve both categories under separate paths.
