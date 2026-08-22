# Contributing

Contributions that improve reproducibility, documentation, validation, or model correctness are welcome after the repository becomes public.

## Before opening a pull request

1. Create a focused branch.
2. Do not change raw CSV matrices or CPN artefacts without documenting provenance and recomputing checksums.
3. Run `pytest -q`.
4. Run the analysis pipeline and confirm that integrity checks pass.
5. Build `manuscript/Manuscript_SMPT.tex`.
6. Update `CHANGELOG.md` and relevant documentation.

## Reporting model or data issues

Use the reproducibility issue template and include:

- operating system and CPN Tools/Python/TeX versions;
- exact model, script, and data checksum;
- command used;
- first error message;
- minimal steps to reproduce.

Do not submit personal, confidential, or unpublished reviewer information.
