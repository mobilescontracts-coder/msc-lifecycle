# Publishing the repository through GitHub and Zenodo

## 1. Create the GitHub repository

Create an empty public repository named `spos-msc-reproducibility`. Do not add
a README or licence through the web interface because this package already
contains them.

From the repository root:

```bash
git init
git branch -M main
git add .
git commit -m "Prepare SPoS-MSC reproducibility package"
git remote add origin https://github.com/<organisation-or-user>/spos-msc-reproducibility.git
git push -u origin main
```

## 2. Resolve release blockers

Before creating the journal-linked release:

```bash
python scripts/import_integrated_cpn.py /path/to/the/exact/integrated/model.cpn
# Add native monitor exports under data/raw/cpn_native/
python scripts/validate_repository.py --strict
```

The strict validator must pass without warnings promoted to failures.

## 3. Record the manuscript commit

After committing every paper-linked artefact:

```bash
git rev-parse HEAD > SUBMISSION_COMMIT.txt
git add SUBMISSION_COMMIT.txt
git commit -m "Record manuscript-linked repository commit"
```

Record the resulting final commit hash in the manuscript data-availability
statement. Do not alter that tag after submission; use a new release for later
changes.

## 4. Prepare the first release

Update:

- `CHANGELOG.md`;
- `CITATION.cff` version and release date;
- `.zenodo.json` metadata;
- manuscript citation/status;
- model/data checksums.

Then:

```bash
make reproduce
make test
make validate-strict
make checksums
git add .
git commit -m "Release v1.0.0"
git tag -a v1.0.0 -m "SPoS-MSC manuscript reproducibility release"
git push origin main --tags
```

Create a GitHub release from tag `v1.0.0` and attach any large archival files
that are not stored directly in Git.

## 5. Archive with Zenodo

1. Sign in to Zenodo using the GitHub-linked account.
2. Enable the GitHub repository in Zenodo's GitHub settings.
3. Publish the GitHub release.
4. Wait for Zenodo to archive the release and mint a DOI.
5. Add the version DOI to the manuscript and the concept DOI to repository
   metadata when appropriate.
6. Update `CITATION.cff` and `.zenodo.json` in the next patch release rather
   than rewriting the archived tag.

## 6. Suggested data-availability statement

> The CPN models, scenario definitions, native monitor exports, prototype
> source code, run-level data, analysis scripts, and figure-generation scripts
> are available in the SPoS-MSC reproducibility repository at the archived DOI.
> The manuscript corresponds to Git commit `<commit-hash>` and release
> `v1.0.0`. CPN-proxy/emulation files and native CPN Tools exports are labelled
> and stored separately.
