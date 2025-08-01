Testing
=======

Supriya uses an extensive test suite to guarantee stability during the
development process.

Install Supriya's test dependencies with:

..  include:: /includes/install-test.txt

Running tests
-------------

Supriya uses `pytest`_ as its test runner, both for unit tests and for
doctests, along with a variety of `pytest_` plugins.

Run `pytest`_ against Supriya's default test paths (:github-tree:`supriya/
<supriya>` and :github-tree:`tests/ <tests>`) with:

..  code-block:: console

    josephine@laptop:~/supriya$ pytest

You can run `pytest`_ against a specific test module with:

..  code-block:: console

    josephine@laptop:~/supriya$ pytest tests/contexts/test_Server_nodes.py

... or against a specific test function in a specific module with:

..  code-block:: console

    josephine@laptop:~/supriya$ pytest tests/contexts/test_Server_nodes.py::test_add_synth

You can also run `pytest`_ against any test or test file matching a pattern
with:

..  code-block:: console

    josephine@laptop:~/supriya$ pytest -k add_synth

See `pytest`_'s complete documentation for a wide variety of invocation
options.

Live servers
````````````

Many unit and doctests run against live SuperCollider servers. Expect to hear
audio during the test run.

If you have any running servers online prior to running the test suite, they
will be automatically killed once the tests start running.

Supriya provides a :py:func:`~supriya.scsynth.kill` function for killing any
process whose name matches ``scsynth``, ``supernova`` or their Windows
equivalents.

Coverage
````````

`pytest`_ can collect code coverage statistics during its test runs via the
`pytest-cov`_ plugin, installed when you install Supriya's test dependencies.

Collect coverage against the code in the :github-tree:`supriya/ <supriya>`
directory during a test run by adding the ``--cov=supriya`` flag:

..  code-block:: console

    josephine@laptop:~/supriya$ pytest --cov=supriya

Supriya provides a ``Makefile`` target to simplify this call:

..  code-block:: console

    josephine@laptop:~/supriya$ make pytest

The coverage report appear at the end of the test output in your terminal:

..  code-block::

    Name                                Stmts   Miss Branch BrPart  Cover
    ---------------------------------------------------------------------
    supriya/__init__.py                    21      4      2      1    78%
    supriya/_version.py                     2      0      0      0   100%
    supriya/clocks/__init__.py              5      0      0      0   100%
    supriya/clocks/asynchronous.py        115      6     40      5    93%
    supriya/clocks/core.py                431     33    118     18    90%
    supriya/clocks/offline.py              97     12     14      4    86%
    supriya/clocks/threaded.py             72      3     22      4    93%
    supriya/contexts/__init__.py            5      0      0      0   100%
    supriya/contexts/allocators.py        154     10     42      8    91%
    supriya/contexts/core.py              532     32    186     22    91%
    supriya/contexts/entities.py          285     41     72     26    78%
    supriya/contexts/nonrealtime.py       113      8     36      5    91%
    supriya/contexts/realtime.py          791     28    262     25    95%
    supriya/contexts/requests.py          718     29    142     14    95%
    supriya/contexts/responses.py         356     12     64      5    96%
    supriya/contexts/scopes.py             94     16     30     15    75%
    supriya/conversions.py                 20      5      0      0    75%
    supriya/enums.py                      381      8     24      3    97%
    supriya/exceptions.py                  36      0      0      0   100%
    supriya/ext/__init__.py                19      6     10      3    62%
    supriya/ext/book.py                    99      2      2      0    98%
    supriya/ext/ipython.py                 23     16      4      0    26%
    supriya/ext/mypy.py                    63     49     18      0    17%
    supriya/io.py                          78     25      8      2    64%
    supriya/osc/__init__.py                 5      0      0      0   100%
    supriya/osc/asynchronous.py            89      8     30      8    85%
    supriya/osc/messages.py               279     35    116     16    85%
    supriya/osc/protocols.py              209     15     68     13    90%
    supriya/osc/threaded.py               115     10     36      7    89%
    supriya/osc/utils.py                   26      5     12      1    84%
    supriya/patterns/__init__.py            7      0      0      0   100%
    supriya/patterns/eventpatterns.py     131     14     42      3    89%
    supriya/patterns/events.py            168     15     52     12    85%
    supriya/patterns/noise.py             114      7     38      8    90%
    supriya/patterns/patterns.py          252      6     54      2    97%
    supriya/patterns/players.py           166     25     60      9    81%
    supriya/patterns/structure.py         157     11     58      7    90%
    supriya/patterns/testutils.py          60      3     22      0    96%
    supriya/sclang.py                      29      7     16      6    67%
    supriya/scsynth.py                    416     29    156     21    91%
    supriya/sessions/__init__.py            6      0      0      0   100%
    supriya/sessions/components.py        241     14     78      9    93%
    supriya/sessions/constants.py          36      2      0      0    94%
    supriya/sessions/devices.py            80      1     16      1    98%
    supriya/sessions/mixers.py             63      2     14      2    95%
    supriya/sessions/sessions.py          200     16     82     15    89%
    supriya/sessions/specs.py             386     50    166     24    83%
    supriya/sessions/tracks.py            363      8    116      7    97%
    supriya/soundfiles.py                  48      7     14      7    77%
    supriya/typing.py                      43      4      0      0    91%
    supriya/ugens/__init__.py              31      0      0      0   100%
    supriya/ugens/basic.py                107      1     48      1    99%
    supriya/ugens/beq.py                   56      0      0      0   100%
    supriya/ugens/bufio.py                 61      0      2      0   100%
    supriya/ugens/chaos.py                162      0      0      0   100%
    supriya/ugens/compilers.py              0      0      0      0   100%
    supriya/ugens/convolution.py           25      0      0      0   100%
    supriya/ugens/core.py                1365     67    492     44    94%
    supriya/ugens/delay.py                128      0      0      0   100%
    supriya/ugens/demand.py               133      2      6      2    97%
    supriya/ugens/diskio.py                15      0      0      0   100%
    supriya/ugens/dynamics.py              32      0      0      0   100%
    supriya/ugens/envelopes.py            259     82     78     18    64%
    supriya/ugens/factories.py            195     20     80     11    87%
    supriya/ugens/ffsinosc.py              36      2      6      3    88%
    supriya/ugens/filters.py              181      0      0      0   100%
    supriya/ugens/gendyn.py                50      0      0      0   100%
    supriya/ugens/granular.py              37      0      0      0   100%
    supriya/ugens/hilbert.py               13      0      0      0   100%
    supriya/ugens/info.py                  47      0      0      0   100%
    supriya/ugens/inout.py                 39      0      2      1    98%
    supriya/ugens/lines.py                 66      1      2      1    97%
    supriya/ugens/mac.py                   25      0      0      0   100%
    supriya/ugens/ml.py                    76      0      0      0   100%
    supriya/ugens/noise.py                119      0      2      1    99%
    supriya/ugens/osc.py                  103      0      0      0   100%
    supriya/ugens/panning.py               89      3      8      3    94%
    supriya/ugens/physical.py              26      0      0      0   100%
    supriya/ugens/pv.py                   196      6      6      0    95%
    supriya/ugens/reverb.py                 7      0      0      0   100%
    supriya/ugens/safety.py                16      1      2      1    89%
    supriya/ugens/system.py               230      5     36      2    97%
    supriya/ugens/triggers.py             148      3      6      3    96%
    supriya/utils/__init__.py               3      0      0      0   100%
    supriya/utils/intervals.py            735     97    324     35    84%
    supriya/utils/iterables.py             86      7     50      7    87%
    ---------------------------------------------------------------------
    TOTAL                               13106    936   3492    471    90%
    Coverage HTML written to dir htmlcov

A line-by-line HTML version of the output can also be found under an ``htmlcov/``
directory at the root of Supriya's codebase.

..  hint::

    Use coverage reporting to guide your test writing. It will expose branches
    that haven't been executed during testing. Aim for 90% coverage, but don't
    stress about going significantly higher. Higher percentages (while often
    possible!) tend to require contortions of logic, and in practice don't
    necessarily yield better stability. Rely on static type-checking to fill in
    the gaps in test coverage.

Writing tests
-------------

..  note::

    The test examples here are in the official test suite, to ensure that they
    continue to work and are also therefore subject to the same formatting,
    linting and static-typing checks as any other code in Supriya. You can find
    them :github-blob:`here <tests/test_examples.py>`.

Some philosophy
```````````````

Whenever possible, keep tests simple:

- some setup (pushed into fixtures if at all possible)
- possibly validate pre-conditions
- perform the operation under test (a single operation!)
- validate post-conditions
- some teardown (pushed into fixtures if at all possible)

Test every public function, even public class, every public method on every
public class. One test per function or method (including initializers if those
are complex, which they shouldn't be if possible). When testing variations on
the same category of behavior, use parameterization.

It's easy to test operations against live, running servers, so make use of
that. Don't *mock* the server, just *use* one. In general, assume that
SuperCollider will behave as expected, allowing yourself to test communication
with the server rather than target server state. SuperCollider doesn't make it
particularly easy to truly validate server state, so prefer to rely on
validating communication instead.

Make sure to test not only *happy* paths, but *unhappy* ones too. If a function
can raise exceptions, test for them. If a function can issue warnings, test for
them. If a function *explicitly* emits logs, test for them. Failure states are
part of the API.

Doctests are OK, but keep them very concise. Prefer to push extended testing in
docstrings into the unit testsuite instead. Prefer to push extensive exposition
into the documentation instead.

..  self-criticism::

    You'll see in some of Supriya's older tests - especially for SynthDefs -
    multiple rounds of operations and validations. Avoid this pattern when
    writing new ones. These older tests will eventually get refactored,
    typically into parametrized tests.

An example test
```````````````

Let's create a simple test that:

- *as setup*, boots a server
- queries the server's node tree
- asserts that the node tree matches our expectations
- *as teardown*, quits the server

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_basic

Not particularly interesting or necessarily useful, but it's a good
demonstration of what a test might look like.

You can run this test with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_basic

Our first test has a problem: if the ``assert`` fails (it won't, but *if it
did*), the server won't quit. Philosophically, booting and quitting the server
aren't even part of what we want to test. Let's solve this, and simplify the
test at the same time. 

Testing with fixtures
`````````````````````

One might be tempted to use a try/finally block to ensure the server quits,
even if the assertion fails. And it's true, that will work fine:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_try_finally

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_try_finally

But there's a simpler way to do this, with less indentation, where we can
extract out the server lifecycle from the test entirely into a reusable
component: a `pytest fixture
<https://docs.pytest.org/en/stable/explanation/fixtures.html>`_.

The following demonstrates a fixture that instantiates a server, boots it,
yields the server for usage elsewhere, and then quits it when that usage
completes:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: server

Importantly, the code *after* the yield will run even if the code using the
yielded server fails. This single-yield generator effectively describes a
setup/test/teardown lifecycle.

We integrate the ``server`` fixture into a test by adding an argument *with the
same name as the fixture* to the test function:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_fixtures

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_fixtures

The resulting test is a little shorter (not dramatically so, but you can
imagine how this saves a lot of space in more complex scenarios), and a little
clearer. We no longer have to handle setup and teardown inside the test, and
have a re-usable fixture we can integrate with other tests in the same
testsuite. The ``server`` fixture will execute once for each test that
references it, allowing us to re-use server functionality, but with strong
isolation due to separate server objects.

Testing async code
``````````````````

Async code *typically* needs to be run inside async tests. To do this:

- Add the ``async`` keyword to the test function definition, like any other
  async function.

- Add the ``@pytest.mark.asyncio`` decorator to the function
  (available via the `pytest-asyncio`_ plugin)

- Use the ``@pytest_asyncio.fixture`` (available via the `pytest-asyncio`_
  plugin) to decorate async fixtures, in this case to decorate a fixture
  returning an :py:class:`~supriya.contexts.realtime.AsyncServer`

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: async_server

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_async

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_async


Note that ``test_async`` looks just like ``test_fixtures``, just... *async*.

Testing async and sync code together
````````````````````````````````````

When testing classes with "mirror" sync and async interfaces, like
:py:class:`~supriya.contexts.realtime.Server` and
:py:class:`~supriya.contexts.realtime.AsyncServer` we can use a little helper
function to optionally await as necessary:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: get

And we can use a (more complex) *async* fixture (available via the
`pytest-asyncio`_ plugin) to instantiate, boot, yield, then quit *either* a
:py:class:`~supriya.contexts.realtime.Server` or a
:py:class:`~supriya.contexts.realtime.AsyncServer`:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: context

The above fixture actually causes tests using it to run *once per value* in the
fixture's ``params`` list, effectively parametrizing the test!

Then we can use the fixture, just like we used the ``server`` fixture
previously, along with the ``get()`` helper, to test that both flavors of
server handle querying the node tree the same way:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_async_and_sync

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_async_and_sync

..  note::
   
    Note the bracketed arguments in the `pytest`_ output. These show (if
    possible) a representation of the parametrized argument(s) to each
    individual run of the test.

Testing node trees diffs
````````````````````````

Many client operations change the state of the server's node tree, and in those
cases the simplest thing to test is often not just "does the node tree look
like what we expect?" but "does the diff of the node tree before and after my
operation look like what I expect?"

To do this, we can literally compare the node tree *before* and *after* an
operation, as a diff. First, query the tree as a pre-condition, query it again
after performing an operation, diff the two strings, and compare your expected
diff against the actual diff.

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_node_tree_diff

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_node_tree_diff

Now, note that there's a lot of boilerplate in that test. Let's extract out the
tree querying and diffing logic into something separate. Because there's
"before" and "after" concepts at play, a context manager is a logical choice
for the extracted logic.

And we'll go one step further, combining the ``get()`` helper we introduced
earlier for testing both sync and async code "homogenously" to create an *async
context manager* that can validate the node tree diff for both sync and async
servers:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: assert_node_tree_diff

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_node_tree_diff_context_manager

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_node_tree_diff_context_manager

..  note::

    If the diff comparisons fail, `pytest`_ will show you a *diff of diffs* in
    its failure reporting. That's not the easiest thing to read, but I swear
    you'll get used to it.

Testing OSC transcripts
```````````````````````

We can validate what OSC messages have been sent to the server via a transcript
:py:class:`~supriya.osc.protocols.Capture`. While this doesn't guarantee that
the resulting server state is correct, it does help us validate that our
communications were what we expected.

Supriya provides a low-level context manager - accessible via the server's OSC
protocol object - for capturing OSC data *sent to* and *received from* the
server:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_osc_transcript

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_osc_transcript

..  note::

    The OSC "transcript" can be filtered via various boolean flags:

    - If ``sent=True`` then the filtered messages will include outgoing OSC
      messages.

    - If ``received=True`` then the filtered messages will include incoming OSC
      messages.

    - If ``status=False`` then nthe filtered messages will omit both
      ``/status`` and ``/status.reply`` messages, as these are constantly being
      sent and received during the course of normal operation.

Testing server process transcripts
```````````````````````````````````

Like the OSX transcript described above, we can also capture ``stdout`` lines
from a server's underlying ``scsynth`` or ``supernova`` process via a process
:py:class:`~supriya.scsynth.Capture`. There are few uses for this, but it's
available nonetheless:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_process_transcript

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_process_transcript

Testing exceptions
``````````````````

Don't simply test happy paths. If some functionality can and *should* raise
exceptions, validate that those exceptions are raised under the expected
conditions. As library authors, we want to treat failure modes as an important
part of API design.

`pytest`_ provides a ``pytest.raises(...)`` context manager for asserting
exceptions were raised by a code block:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_exceptions

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_exceptions

Testing warnings
````````````````

Like exceptions, we should also test for any warnings our code explicitly
raises.

`Python`_'s standard library provides a
``warnings.catch_warnings(record=True)`` context manager for catching warnings
we can inspect later:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_warnings

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_warnings

Testing logs
````````````

We can also test for logging output. Why write logging code if you don't verify
that it logged the way you want?

`pytest`_ provides a `caplog fixture
<https://docs.pytest.org/en/stable/how-to/logging.html#caplog-fixture>`_
that lets you set logging levels and capture logs during tests:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_logging

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_logging

Testing parametrically
``````````````````````
Last, but not least. Often you'll write a series of very similar tests, and
it's often the case that with some careful considerations you can transform
that series of similar tests into a single test with varying inputs. This is a
"parametrized" test: one test body, but a series of one or more varying sets of
inputs.

..  note::
   
    The `pytest`_ folks use the British "parametrize" spelling rather than the
    American "parameterized" spelling. We'll use the same spelling they do for
    the sake of consistency.

You can create a parametrized test with the ``@pytest.mark.parametrize``
`decorator
<https://docs.pytest.org/en/stable/how-to/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions>`_.
This decorator has two arguments:

- A string containing comma-delimited names which must map to arguments to your
  test function

- A list of arguments, or tuples of arguments the same length as the number of
  names defined in the preceding string

We can demonstrate this with a long - but ultimately simple - test combining
some of the techniques previously described above. What is the node tree diff
when we add a new group relative to an old one, with the ``add_action`` varying
in each test scenario?

To test this we need two parametrized arguments: the add action under test, and
the expected output. Then we'll craft a sequences of test scenarios, one for
each add action, with a matching expected node tree diff. The test body will
execute its logic with each different add action, and validate that our
expected node tree diff matches the actual node tree diff:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_parametrized

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_parametrized

Parameters are combinatoric. You can use multiple ``@pytest.mark.parametrize``
decorators and/or parametrized fixtures with the same test case, and `pytest`_
will perform combinatoric expansion. Let's use the ``context`` fixture defined
earlier that can yield either a sync or async server with our initial
parametric test cases:

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_parametrized_combinatoric

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_parametrized_combinatoric

Note the expansion in the test report: five add actions times two server types.

..  note::

    Debugging parametrized tests can be difficult because of the verticality of
    the code, and the non-obvious connection between which parameter block was
    associated with which failure. In general, try not to stack too many
    different parametric groups, simply for the sake of legibility.

Testing parametrically with fixtures
````````````````````````````````````

One thing parametrized tests are not good at is handling parametrized fixtures.
By default, `pytest`_ won't expand fixture references that are arguments to a
parametrized test scenario. However, we can use the `pytest-lazy-fixtures`_
plugin's ``lf`` function to lazily evaluate fixtures appearing in a
parametrized scenario.

As an example, let's replace the ``context`` fixture - which expands to either
a :py:class:`~supriya.contexts.realtime.Server` or
:py:class:`~supriya.contexts.realtime.AsyncServer` - with another
``@pytest.mark.parametrize`` decorator whose arguments are lazily-evaluated
references to the ``async_server`` and ``server`` fixtures.

..  literalinclude:: ../../../tests/test_examples.py
    :pyobject: test_parametrized_lazy_fixtures

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    pytest tests/test_examples.py::test_parametrized_lazy_fixtures

..  note::

    There's no good reason to do this specifically except for the sake of
    pedagogy. The original ``context`` fixture is cleaner, but we need to
    demonstrate the lazy technique.

Formatting
----------

Supriya follows PEP8 formatting standards. While Supriya originally used a
combination of `black`_ and `isort`_ to handle formatting code and sorting
imports, it now just uses `ruff`_.

You can auto-format the codebase with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    make reformat

Linting
-------

While Supriya originally used `flake8`_ for linting, it now uses `ruff`_, for
sake of speed and ease of configuration.

You can lint the codebase with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    make ruff-lint

Type-checking
-------------

Supriya employs static type-checking extensively (although this is always a
work-in-progress) and uses `mypy`_ to perform the analysis.

You can run static type-checking with:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    make mypy

When writing (or refactoring) code, make sure to add type hints whenever
possible. Except in rare cases - typically extremely dynamic programming or
low-level systems programming-, most functions and methods can be type hinted.
We aim for every method and function to *at least* have a return value, but
more is better.

..  note::

    Also make sure to type hint tests in the test suite, as this makes
    refactoring the codebase simpler and surfaces errors faster than simply
    running the tests.

Mypy extensions
```````````````

Because of its use of metaclasses for code generation in UGens, Supriya
requires a `mypy`_ extension to teach it about the auto-generated methods and
properties on those classes.

The extension lives in :github-blob:`supriya/ext/mypy.py <supriya/ext/mypy.py>`
and MyPy is already configured to use it via the ``plugins`` field in Supriya's
:github-blob:`pyproject.toml <pyproject.toml>`.

Should you need to type check against Supriya's UGens in another project, you
can activate the `mypy`_ extension with the following code:

..  code-block:: toml

    [tool.mypy]
    plugins = ["supriya.ext.mypy"]

CI/CD
-----

Every push to Supriya's `GitHub`_ repository runs the GitHub Actions `test
workflow
<https://github.com/supriya-project/supriya/actions/workflows/test.yml>`_.

This workflow does *a lot* of different validations:

- It builds SuperCollider from source under Ubuntu, OSX *and* Windows

- It configures dummy sound-cards under each of those operating systems and
  gut-checks that the SuperCollider server can boot

- It builds the Sphinx documentation (which requires SuperCollider!) and checks
  every external link found in the documentation to ensure nothing is broken

- It builds the same wheels that would be published to PyPI to prove that
  package publishing is possible on the current commit

- It format-checks, lints and type-checks the entire codebase, including the
  test suite

- It gut-checks that Supriya is installable and importable without any of its
  optional dependencies

- It gut-checks that Supriya's shared memory works

- It runs `pytest`_ against both the unit tests and doctests under all
  operating systems and all major, non-end-of-life, non-alpha versions of
  Python (e.g. 3.10, 3.11, 3.12, 3.13)
