.PHONY: docs

black-check:
	black --py36 --check --diff supriya/ tests/

black-reformat:
	black --py36 supriya/ tests/

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif .cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif prof/
	rm -Rif supriya.egg-info/

docs:
	make -C docs/ html

isort:
	isort --multi-line 1 --recursive --thirdparty uqbar --thirdparty abjad --trailing-comma --use-parentheses -y supriya/ tests/

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
		--profile \
		--timeout=60 \
		tests/ \
		supriya/

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
		tests/ \
		supriya/

reformat:
	make isort
	make black-reformat
