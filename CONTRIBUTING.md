# Contributing

Contributions that improve reproducibility, provenance, documentation, or test coverage are welcome.

## Before opening a pull request

1. Create a branch from `main`.
2. Run `pytest -q`.
3. Run `python scripts/validate_repository.py`.
4. Do not replace raw data silently. Add a provenance note and checksum.
5. Do not label proxy/emulation results as native CPN Tools monitor exports.
6. Keep scenario identifiers Q1–Q7 and metric definitions stable unless the manuscript is updated simultaneously.

## Reporting discrepancies

Open an issue containing:

- the file and commit hash;
- the command executed;
- the expected and observed result;
- Python, operating-system, or CPN Tools version;
- relevant log excerpts.
