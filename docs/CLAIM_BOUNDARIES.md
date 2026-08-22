# Evidence and claim boundaries

The repository deliberately separates what the supplied artefacts demonstrate from what remains outside scope.

## Supported by the supplied artefacts

- Executable lifecycle reachability for the reported runs.
- Run-observed ordering and terminal-accounting invariants.
- Bounded Q1–Q7 scenario behaviour at four shards.
- Local three-level sensitivity for eight executable controls.
- Run-level lifecycle, load, governance, reward and concentration metrics.
- Reproduction of the published statistical tables and figures from raw CSV matrices.
- Directional comparison with seven manuscript-level runtime-emulator scenario means.

## Not established

- Public-network blockchain throughput or latency.
- Shard-count scale-out across 1/2/4/8 or more shards.
- Global parameter sensitivity or complete uncertainty quantification.
- Higher-order factor interactions.
- Causal superiority over stake-only, static-routing, no-recovery, Round-Robin or other unexecuted baselines.
- Exhaustive state-space verification.
- Concrete cryptographic, peer-to-peer network, or production root-chain correctness.
- Multi-epoch prevention of stake oligopoly.
- Fully reproducible runtime-emulator execution, because its source and raw outputs are not in the supplied package.

The CPN `nakamoto_coefficient` field is a reward-based 51% concentration measure recorded by the model; it is not a direct estimate of real-network takeover power.
