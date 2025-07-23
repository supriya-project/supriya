Testing
=======

Supriya uses an extensive test suite to guarantee behavior and stability during
the development process.

Install Supriya's test dependencies with:

.. include:: /includes/install-test.txt

Running tests
-------------

Supriya uses `pytest`_ as its test runner, both for unit tests and for
validating doctests.

- currently using pytest with a variety of plugins
- coverage

.. code-block:: bash

   supriya$ pytest

Coverage
````````

.. code-block:: bash

   supriya$ pytest --cov=supriya

- coverage report
- coverage location

Writing tests
-------------

- test against live running servers
- test every public method and function
- avoid mocking
- coverage: aiming for 90%
- doctests are ok, but keep them short
- use pytest.mark.parametrize
- sync and async variants in the same test
- timing-based tests are liable to be flakey
- when testing against the server, test osc communications and server tree state
    - use captures
    - use server tree diffs

Formatting
----------

- formatting is originally based on black and isort
- currently using ruff

Linting
-------

- currently using ruff

Type-checking
-------------

- currently using mypy
- type hint all methods and functions
- type hint test suite too
- supriya.ext.mypy

CI/CD
-----

- github actions
- build supercollider in the pipe
- build the docs
- lint
- run against linux, osx, windows
