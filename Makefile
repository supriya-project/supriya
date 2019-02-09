.PHONY: build docs gh-pages

errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
paths = supriya/ tests/ *.py

black-check:
	black --py36 --check --diff ${paths}

black-reformat:
	black --py36 ${paths}

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif .cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif prof/
	rm -Rif *.egg-info/

docs:
	make -C docs/ html

flake8:
	flake8 --max-line-length=90 --isolated --ignore=${errors} ${paths}

isort:
	isort \
		--multi-line 1 \
		--recursive \
		--thirdparty abjad \
		--thirdparty uqbar \
		--thirdparty yaml \
		--trailing-comma \
		--use-parentheses -y \
		${paths}

mypy:
	mypy --ignore-missing-imports supriya

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=supriya/ \
		--durations=20 \
		--timeout=60 \
		${paths}

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
		${paths}

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
