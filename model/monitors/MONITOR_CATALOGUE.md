# Monitor and Output Catalogue

The final integrated model should expose or export evidence for the following categories. Verify names against the exact submitted `.cpn` file.

| Evidence category | Representative place/output |
|---|---|
| Mobile transactions | input/submitted transaction place |
| Routed transactions | routed shard mempool |
| Validator scores | active validator-score place |
| Active committees | shard committee places |
| Finality | finality certificate archive |
| Root commitment | root-commitment or anchor-evidence place |
| Receipts | output mobile receipts / receipt archive |
| Rewards | validator reward events |
| Slashing/security | misbehaviour evidence and slashing events |
| Load/reconfiguration | shard-load and reconfiguration log |
| Decentralisation | Gini, HHI, Nakamoto, owner/validator reward shares |
| Run metadata | scenario, run, seed, epoch, model/policy identifier |
| Aggregate run result | final result archive / monitor export |

A native export should include one unambiguous row per run and sufficient identifiers to reproduce every table and figure.
