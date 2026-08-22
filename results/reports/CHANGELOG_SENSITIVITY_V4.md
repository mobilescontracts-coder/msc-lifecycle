# Sensitivity-complete manuscript changes

This project integrates the completed SPoS-MSC local sensitivity analysis into the manuscript and presents a public v3-to-v4 artefact sequence.

## Manuscript

- aligns the Abstract, RQ3, contributions, Sections 4-6, conclusion, future work, supplementary statement, and data-availability statement;
- adds the executable sensitivity parameterisation and `P_SensitivityData` provenance path;
- adds the eight-factor, three-level OFAT design table;
- reports 700 v4 scenario replications and 2,400 v4 OFAT replications;
- replaces v3 scenario statistics with the consistent v4 scenario matrix;
- adds local sensitivity tests, effect sizes, controlled contrasts, and the mobile-threshold tipping-point analysis;
- treats OFAT cells as independent repeated-run groups rather than matched pairs;
- retains conservative boundaries for public-network throughput, causal baselines, global sensitivity, formal verification, and shard scale-out;
- removes revision-only prose and maintains present-tense scientific narration in active manuscript text.

## Public artefacts

- renames the final sensitivity-enabled executable to public v4;
- retains v3 only as the predecessor model;
- updates scripts, data filenames, figures, tables, analysis outputs, and checksum records to the public v4 sequence;
- records the internal legacy `DEFAULT_EQ` identifier transparently as a default-configuration audit.
