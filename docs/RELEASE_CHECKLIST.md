# Public and archival release checklist

- [ ] Confirm author names, affiliations, corresponding-author email, and ORCIDs.
- [ ] Approve CRediT contribution statement.
- [ ] Add funding and competing-interest statements.
- [ ] Select and approve repository licences.
- [ ] Add native CPN Tools replication-report/output folders for 2, 72, 700 and 2,400 runs.
- [ ] Add the archived v3 raw 700-row matrix, or state that only its aggregate audit is available.
- [ ] Add reference runtime emulator source, lock file, raw outputs, and execution instructions.
- [ ] Confirm architecture and goal-model editable sources.
- [ ] Create a signed GitHub release tag, preferably `v4.0.0`.
- [ ] Archive the release in Zenodo and update `CITATION.cff` with the DOI.
- [ ] Recompute `CHECKSUMS.sha256` after all author-supplied additions.
- [ ] Run GitHub Actions and local `make all` successfully.
