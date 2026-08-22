# Manuscript build

Set `Manuscript_SMPT.tex` as the Overleaf main file. The folder is self-contained and uses Elsevier's CAS single-column template.

Local build:

```bash
SOURCE_DATE_EPOCH=1787011200 latexmk -pdf Manuscript_SMPT.tex
```

The included PDF is the reference build supplied with the reproducibility release.

The fixed `SOURCE_DATE_EPOCH` makes the supplied PDF byte-reproducible when the same TeX Live/BibTeX environment is used.
