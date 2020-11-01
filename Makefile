.PHONY: build docs gh-pages

project = supriya
errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

black-check:
	black --target-version py36 --check --diff ${formatPaths}

black-reformat:
	black --target-version py36 ${formatPaths}

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .*cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/

docs:
	make -C docs/ html

docs-clean:
	make -C docs/ clean html

flake8:
	flake8 --isolated --ignore=${errors} ${formatPaths}

gh-pages: docs-clean
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

isort:
	isort \
		--case-sensitive \
		--multi-line 3 \
		--skip supriya/__init__.py \
		--thirdparty uqbar \
		--thirdparty yaml \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

mypy:
	mypy --ignore-missing-imports ${project}/

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		--timeout=60 \
		${testPaths}

pytest-x:
	rm -Rf htmlcov/
	pytest \
		-x \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=supriya/ \
		--durations=20 \
		--timeout=60 \
		${testPaths}

reformat:
	make isort
	make black-reformat

release:
	make test
	make clean
	make build
	twine upload dist/*.tar.gz
	make gh-pages

test:
	make black-check
	make flake8
	make mypy
	make pytest
