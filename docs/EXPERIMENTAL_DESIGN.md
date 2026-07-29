# Experimental design

## Evidence layers

### 1. Formal model artefacts

The CPN models define typed protocol states, guards, token dependencies, and
hierarchical execution. Structural arguments concern routing integrity,
committee-dependent finality, quarantine exclusion, receipt-after-commitment
evidence, and overload observability.

### 2. Scenario-based CPN evidence

The journal release should include native CPN Tools monitor exports for Q1–Q7.
The workbooks currently committed under `data/raw/cpn_proxy/` are retained only
as labelled proxy/emulation data and must not be represented as native CPN
output.

### 3. Prototype evidence

The prototype executes the complete scenario workflow and reports run-level
wall-clock and lifecycle metrics. Its throughput is a controlled single-host
processing measurement, not public-network blockchain TPS.

## Unit of analysis

One run is the primary statistical unit. Individual transactions, receipts,
or reward events within a run are not treated as statistically independent
replicates.

## Repetitions

- Seven scenarios (Q1–Q7)
- 100 runs per scenario
- 700 observations per evidence layer

## Statistical summaries

For each run-level metric, report:

- arithmetic mean;
- sample standard deviation;
- median;
- first and third quartiles;
- 95% Student-t confidence interval.

## Controlled comparisons

Direct performance claims should use internally controlled variants sharing
the same workload and measurement definitions. External systems are used only
for metric-level context unless an identical experimental setup is reproduced.
