.PHONY: docs

clean:
	rm -Rif __pycache__
	rm -Rif supriya.egg-info/
	rm -Rif dist/
	rm -Rif build/
	rm -Rif .tox/
	rm -Rif .cache/
	rm -Rif prof/
	find . -name '*.pyc' | xargs rm

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
		-x \
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
