.PHONY: install test lint reproduce validate validate-strict checksums run api docker release

install:
	python -m pip install -r requirements-dev.txt

test:
	pytest -q

lint:
	ruff check spos_msc scripts analysis tests

reproduce:
	python analysis/summarise_cpn_proxy.py
	python analysis/summarise_prototype.py
	python analysis/generate_figures.py

validate:
	python scripts/validate_repository.py

validate-strict:
	python scripts/validate_repository.py --strict

checksums:
	python scripts/generate_checksums.py

run:
	python scripts/run_scenarios.py --runs 100 --seed 626 --output outputs

api:
	uvicorn spos_msc.main:app --host 0.0.0.0 --port 8000

docker:
	docker compose up --build

release:
	bash scripts/make_release.sh
