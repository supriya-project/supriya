.PHONY: build docs gh-pages

project = supriya
errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

black-check:
	black --py36 --check --diff ${formatPaths}

black-reformat:
	black --py36 ${formatPaths}

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif .*cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif prof/
	rm -Rif *.egg-info/

docs:
	make -C docs/ html

flake8:
	flake8 --max-line-length=90 --isolated --ignore=${errors} ${formatPaths}

isort:
	isort \
		--multi-line 1 \
		--recursive \
		--thirdparty abjad \
		--thirdparty uqbar \
		--thirdparty yaml \
		--trailing-comma \
		--use-parentheses -y \
		${formatPaths}

mypy:
	mypy --ignore-missing-imports ${project}/

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=supriya/ \
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
	make clean
	make build
	twine upload dist/*.tar.gz

test:
	make black-check
	make flake8
	make mypy
	make pytest
