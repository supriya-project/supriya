.PHONY: docs

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
	make -C docs html

sanity-check:
	python -c 'import supriya; server = supriya.Server().boot(); print(server); server.quit()'

test:
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

test-travis:
	pytest \
		--durations=100 \
		--profile \
		--timeout=60 \
		tests/test_realtime_Server_boot.py \
		tests/ \
		supriya/

testx:
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

mypy:
	mypy supriya ../uqbar/uqbar ../../Abjad/abjad/abjad ../../Abjad/abjad-ext-tonality/abjadext
