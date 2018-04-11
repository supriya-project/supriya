clean:
	rm -Rif __pycache__
	rm -Rif supriya.egg-info/
	rm -Rif dist/
	rm -Rif build/
	rm -Rif .tox/
	rm -Rif .cache/
	rm -Rif prof/
	find . -name '*.pyc' | xargs rm
