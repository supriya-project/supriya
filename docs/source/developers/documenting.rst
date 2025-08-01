Documentating
=============

Install Supriya's documentation dependencies with:

..  include:: /includes/install-docs.txt

Building documentation
----------------------

Supriya's `Sphinx`_ documentation lives under :github-tree:`docs/`.

You can build the documentationg with:

..  code-block:: console

    josephine@laptop:~/supriya$ make docs

In rare cases, some docs artifacts may become stale. In that case, blow away
the build artifacts and rebuild fresh with:

..  code-block:: console

    josephine@laptop:~/supriya$ make docs-clean

GitHub Pages
````````````

When publishing a new release on `GitHub`_, a `GitHub Actions
<https://github.com/supriya-project/supriya/actions>`_ pipeline will
automatically build Supriya's `Sphinx`_ documentation and push it GitHub Pages.

The resulting docs are then available online at
https://supriya-project.github.io/supriya.

Writing documentation
---------------------

Writing docs has historically been the most difficult and neglected aspect of
this project, so - with grace - some guidance.

sphinx
``````

Supriya's documentation is built via `Sphinx`_ and, both under
:github-tree:`docs/` and in every docstring, uses `reStructuredText
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
formatting.

..  note::

    reStructuredText is uglier than Markdown, more complicated, and also *far,
    far* more extensible and expressive. The majority of Sphinx's interesting
    features like custom directives, plugins, cross-references, etc. require
    reStructuredText capabilities. While Markdown is used sparingly in READMEs
    only intended for viewing on GitHub (e.g. the :github-blob:`root README
    <README.md>`), everywhere else should use reStructuredText.

Familiarize yourself with reStructuredText's basics, and with its `Python
domain <https://www.sphinx-doc.org/en/master/usage/domains/python.html>`_
before attempting to write any documentation.

sphinx-immaterial
`````````````````

Supriya uses the `sphinx-immaterial`_ theme, based on the storied
`mkdocs-material`_ theme written for `mkdocs`_ and Markdown, because it's
beautiful and quite powerful.

uqbar.sphinx.api
````````````````

API documentation is pulled into `Sphinx`_ during the docs build process via
the `uqbar.sphinx.api`_ extension. New files will be created, existing files
updated, and stale files removed automatically. You do not need to manually
generate or manage reStructuredText files for API documentation. Just make sure
to write docstrings!

uqbar.sphinx.book
`````````````````

All code examples in the documentation - including code examples in docstrings
- are executed during the documentation build process, and their console
outputs (and sometimes media outputs) captured into the built docs. We do this
to guarantee code examples are always up-to-date with the most recent version
of the code.

Supriya uses the `uqbar.sphinx.book` extension to accomplish this process. Every
"document" in the documentation effectively gets its own console session, much
like a `Jupyter`_ notebook. Code blocks are interpreted in this session, in the
order they appear in the document. If any code block raises an unhandled
exception, the build process will fail.

..  important::

    Code blocks in docstrings pulled from Python modules should not rely on
    maintaining state across as the order they appear in the Python module is
    not guaranteed to be the same order they appear in the doctree. Unlike in
    doctests, ``uqbar.sphinx.book`` will not automatically import the contents
    of the Python module into the console global namespace, so make sure
    imports are fully qualified.

..  important::

    Supriya's interpreted docs all automatically receive the import ``import
    supriya`` at the very beginning of their interpreter sessions.

`uqbar.sphinx.book`_ provides some explicit `Sphinx`_ directives for
finer-grained control over output formatting and error handling.

A ``.. book::`` block without arguments is effectively the same as `Sphinx`_'s
``.. code-block::``:

..  rst-example:: A book block

    ..  book::

        >>> print("this is basically the same as a ``.. code-block::``")

However, sometimes it's helpful to perform some setup or teardown in the midst
of a document without showing the work. Use the ``:hide:`` option to omit both
the interpreter textual input and output for a single block.

..  rst-example:: Hiding code

    ..  book::
        :hide:

        >>> hidden_server = supriya.Server()  # executed, but hidden from Sphinx output

Audio and visual output from hidden ``.. book::`` blocks will still be
rendered, although any textual input and/or output from those blocks will be
hidden:

..  rst-example:: Hiding code, but showing visuals

   ..  book::
       :hide:

       >>> supriya.graph(supriya.default)

``uqbar.sphinx.book`` maintains state across interpreted blocks, including
hidden ones:

..  rst-example:: Implicit Python code blocks

    ::

        >>> print(hidden_server)  # knows about ``hidden_server`` from before

..  rst-example:: Explicit Python code blocks

    ..  code-block:: python

        >>> print(repr(hidden_server.boot_status))  # also knows about ``hidden_server``

Exceptions should be either handled explicitly in the code blocks, or
safe-listed via the ``:allow-exceptions:`` flag:

..  rst-example:: Allowing exceptions

    ..  book::
        :allow-exceptions:

        >>> print(1 / 0)  # this will blow up, but won't break the docs

Finally, shell console sessions can be captured, just like Python sessions:

..  rst-example:: Shell sessions

    ..  shell::
        :cwd: ..
        :rel: ..
        :user: josephine
        :host: laptop

        echo "hello, world!"

Docstrings
``````````

Every public module, public class, public method and property on every public,
and public function should receive a docstring of at least one sentence.

The first sentence of every package or module docstring should be a phrase
summaring the contents or purpose of the module:

- "*Tools for interacting with scsynth-compatible execution contexts.*"

The first sentence of every class docstring should be a phrase giving the
simple English singular description of the class:

- "*A server.*"

This may be followed by additional phrases or sentences providing additional
color.

The first sentence of every function, method and property docstring should be
in the `imperative mood <https://en.wikipedia.org/wiki/Imperative_mood>`_ -
*the grammatical mood that forms a command or request* - and end in a period.

- "*Get* boot status"
- "*Boot* the server"
- "*Quit* the server"
- "*Kill* running servers"

When referring to the "self" object in a class method or property, use "the"
and a lower-case common English name of the class to refer to itself:

- "Boot *the* server"

If it's necessary to draw a distinction between the "self" and another instance
of the same class, you may use "this" and "other":

- "Merge *this* server's options with *other* server's options"

When documenting functions, methods and properties (including class
initializers), use `info field lists
<https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists>`_:

- Argument names and descriptions: ``:param <param name>: <param description>``
- Exception raising descriptions: ``:raises <error-type>: <error description>``
- Return descriptions: ``:return: <return description>``

Don't worry about explicitly adding types to the documentation. `Sphinx`_ will
pull type annotations directly out of the Python source code.

Writing examples
----------------

Supriya's examples live in :github-tree:`examples/`.

Each example should receive its own subdirectory (named e.g.
``examples/hello_world/``), its own ``README.md`` with basic usage information,
and one (and preferably only one) Python module named the same as the directory
(named e.g. ``examples/hello_world/hello_world.py``).

There should also be a reStructuredText document named after the example in the
documentation source (e.g. ``docs/source/examples/hello_world.rst``) and
included into the examples TOC (table-of-contents) in the root reStructuredText
:github-blob:`index.rst <docs/source/index.rst>`.

Each example Python module should have a ``main()`` function, and an ``if
__name__ == "__main__":`` block executing it:

..  code-block:: python

    def main() -> None:
        print("this is an *example* example.")

    if __name__ == "__main__":
        main()

If the example requires additional command-line arguments, use ``argparse``
with the argument parser setup and argument parsing wrapped into its own
function.

Besides any top-level imports and the ``if __name__ == "__main__":`` block,
everything in the example should be a function or class. Why? These constructs
play well with Sphinx's ``.. literalinclude::`` directive, which is able to
target specific classes or functions by name when including Python code into
documentation. Unfortunately, ``.. literalinclude::`` can't target data objects
except via line numbers, and line numbers are not a semantic.

Using an alternating series of prose blocks and ``.. literalinclude::`` blocks,
describe the entire example module in the accompanying reStructuredText.
