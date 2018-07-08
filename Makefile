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

test:
	pytest --cov=supriya --cov-report=html --cov-report=term --cov-branch supriya tests
