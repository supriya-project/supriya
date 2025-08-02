.PHONY: build docs gh-pages
.DEFAULT_GOAL := help

project = supriya
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ docs/ examples/ tests/ *.py
mypyPaths = ${project}/ examples/ tests/
testPaths = ${project}/ tests/

help: ## This help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Clean-out transitory files
	find . -name '*.pyc' | xargs rm
	find . -name '.ipynb_checkpoints' | xargs rm -Rf
	rm -Rif *.egg-info/
	rm -Rif .*cache/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/
	rm -Rif wheelhouse/

docs: ## Build documentation
	make -C docs/ html

docs-clean: ## Build documentation from scratch
	make -C docs/ clean html

lint: reformat ruff-lint mypy ## Run all linters

mypy: ## Type-check via mypy
	mypy ${mypyPaths}

mypy-cov: ## Type-check via mypy with coverage reported to ./mypycov/
	mypy --html-report ./mypycov/ ${mypyPaths}

mypy-strict: ## Type-check via mypy strictly
	mypy --strict ${mypyPaths}

pytest: ## Unit test via pytest
	pytest ${testPaths} --cov=supriya

reformat: ruff-imports-fix ruff-format-fix ## Reformat codebase

ruff-format: ## Lint via ruff
	ruff format --check --diff ${formatPaths}

ruff-format-fix: ## Lint via ruff
	ruff format ${formatPaths}

ruff-imports: ## Format imports via ruff
	ruff check --select I,RUF022 ${formatPaths}

ruff-imports-fix: ## Format imports via ruff
	ruff check --select I,RUF022 --fix ${formatPaths}

ruff-lint: ## Lint via ruff
	ruff check --diff ${formatPaths}

ruff-lint-fix: ## Lint via ruff
	ruff check --fix ${formatPaths}
