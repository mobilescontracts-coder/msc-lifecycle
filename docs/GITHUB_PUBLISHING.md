# Publish the prepared repository to GitHub

The repository target recorded in the manuscript is:

```text
https://github.com/mobilescontracts-coder/spos-msc
```

A Git repository and signed-style annotated release tag are already prepared in the downloadable bundle. To publish the working tree manually:

```bash
cd spos-msc
git remote add origin https://github.com/mobilescontracts-coder/spos-msc.git
git push -u origin main
git push origin v4.0.0
```

Where the remote repository already contains commits, inspect and reconcile its history before pushing; do not use a force push without reviewing the remote state.

## Recommended GitHub settings

- Enable Issues and Discussions for reproducibility reports.
- Protect `main` and require the analysis, checksum, and manuscript workflows.
- Create release `v4.0.0` from the prepared tag.
- Attach the source archive and compiled manuscript PDF to the release.
- Connect the repository to Zenodo only after the authors approve the licence and final metadata.
- Replace repository-only availability text with the archival DOI after Zenodo mints it.
