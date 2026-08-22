PYTHON ?= python3

.PHONY: all verify analysis reference-check test manuscript clean

all: verify test analysis reference-check manuscript

verify:
	sha256sum --check CHECKSUMS.sha256

analysis:
	$(PYTHON) analysis/analyze_spos_msc_v4.py \
	  --smoke-csv data/raw/cpn/SPoS_MSC_v4_smoke_2.csv \
	  --pilot-csv data/raw/cpn/SPoS_MSC_v4_sensitivity_pilot_72.csv \
	  --default-csv data/raw/cpn/SPoS_MSC_v4_default_configuration_audit_700.csv \
	  --ofat-csv data/raw/cpn/SPoS_MSC_v4_sensitivity_OFAT_2400.csv \
	  --output-dir analysis/reproduced

reference-check: analysis
	$(PYTHON) analysis/verify_reference_outputs.py --generated analysis/reproduced --reference analysis/reference_outputs

test:
	$(PYTHON) -m pytest -q

manuscript:
	cd manuscript && SOURCE_DATE_EPOCH=1787011200 latexmk -pdf Manuscript_SMPT.tex

clean:
	rm -rf analysis/reproduced analysis/ci-output .pytest_cache
	cd manuscript && latexmk -C Manuscript_SMPT.tex || true
