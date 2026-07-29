# Integrated CPN Model

Copy the exact manuscript-linked integrated model here using:

```bash
python scripts/import_integrated_cpn.py /path/to/SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn
```

Expected destination:

```text
SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn
```

The importer checks that the file is CPN XML, reports the CPN Tools version, searches for SPoS-MSC integration declarations, and generates a SHA-256 checksum.
