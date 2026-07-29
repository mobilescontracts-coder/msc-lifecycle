# Release and Zenodo Checklist

## Repository finalisation

- [ ] Resolve every item in `docs/RELEASE_BLOCKERS.md`.
- [ ] Run `make release` after all release blockers are resolved.
- [ ] Review `checksums/SHA256SUMS`.
- [ ] Confirm author names and ORCIDs in `CITATION.cff` and `.zenodo.json`.
- [ ] Create `SUBMISSION_COMMIT.txt` from the final commit.
- [ ] Tag the version, for example `v1.0.0`.
- [ ] Create a GitHub release with a concise changelog.

## Zenodo

- [ ] Link the GitHub account to Zenodo.
- [ ] Enable the repository in Zenodo before publishing the GitHub release.
- [ ] Publish the GitHub release and wait for Zenodo ingestion.
- [ ] Reserve or obtain the DOI.
- [ ] Add the DOI badge and DOI to `CITATION.cff` and `.zenodo.json`.
- [ ] Commit the DOI metadata and create a metadata-only patch release if required.

## Submission package

- [ ] Cite the versioned DOI in the manuscript data/code availability statement.
- [ ] Include the repository URL and exact commit hash.
- [ ] State which evidence is native CPN, proxy CPN, and prototype output.
