# Statistical analysis

## Unit of analysis

One explicitly completed CPN replication is one observation. Transaction tokens within a run are not treated as independent samples.

## Scenario matrix

For each Q1–Q7 scenario, the analysis reports the mean, sample standard deviation, median, interquartile range, range, and two-sided 95% Student-t confidence interval over 100 run-level observations.

## Sensitivity matrix

Low, default, and high cells are treated as separately executed groups. Corresponding run IDs identify coverage and provenance but do not establish matched random streams.

For each factor's primary response, the analysis reports:

1. Kruskal–Wallis three-level omnibus test.
2. Local effect size
   \[
   \epsilon^2=\frac{H-k+1}{N-k},
   \]
   with \(k=3\) and \(N=300\).
3. Mann–Whitney U contrasts for low versus default and high versus default.
4. Holm correction across the 16 planned contrasts.
5. Cliff's delta.
6. Welch 95% confidence interval for the difference in group means.

The epsilon-squared values measure within-factor separation of a selected response over three tested levels. They are not global parameter-importance indices and are not directly comparable as Sobol-like rankings.

## Derived metrics

- Finality success: `100 * finality_certificates / submitted_tx`
- Receipt success: `100 * receipts / submitted_tx`
- Cross-shard ratio: `100 * cross_shard_tx / submitted_tx`
- Logical throughput: `receipts / model_time`
- Mean finality latency: `finality_latency_sum / finality_latency_n`
- Mean receipt latency: `receipt_latency_sum / receipt_latency_n`
- Gini, HHI, owner share and load SD: corresponding `_bp` field divided by 100
