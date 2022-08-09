.PHONY: build docs gh-pages
.DEFAULT_GOAL := help

project = supriya
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-z0-9A-Z_-]+:.*?## / {printf "\033[36m%-30s\033]0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

black-check: ## Check syntax via black
	black --check --diff ${formatPaths}

black-reformat: ## Reformat via black
	black ${formatPaths}

build: ## Build for distribution
	python setup.py sdist

clean: ## Clean-out transitory files
	find . -name '*.pyc' | xargs rm
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

flake8: ## Lint via flake8
	flake8 ${formatPaths}

gh-pages: docs-clean ## Build and publish documentation to GitHub
	rm -Rf gh-pages/
	git clone $(origin) gh-pages/
	cd gh-pages/ && \
		git checkout gh-pages || git checkout --orphan gh-pages
	rsync -rtv --del --exclude=.git docs/build/html/ gh-pages/
	cd gh-pages && \
		touch .nojekyll && \
		git add --all . && \
		git commit --allow-empty -m "Update docs" && \
		git push -u origin gh-pages
	rm -Rf gh-pages/

isort: ## Reformat via isort
	isort ${formatPaths}

lint: reformat flake8 mypy ## Run all linters

mypy: ## Type-check via mypy
	mypy ${project}/

pytest: ## Unit test via pytest
	rm -Rf htmlcov/
	pytest ${testPaths}

reformat: ## Reformat codebase
	make isort
	make black-reformat

release: ## Release
	make test
	make clean
	make build
	twine upload dist/*.tar.gz
	make gh-pages

test: ## Test
	make black-check
	make flake8
	make mypy
	make pytest
