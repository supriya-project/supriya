Documentating
=============

Install Supriya's documentation dependencies with:

.. include:: /includes/install-docs.txt

Building documentation
----------------------

Supriya's documentation lives under :github-tree:`docs/`.

sphinx
``````

- restructured text
- make docs
- make docs-clean

uqbar.book
``````````

- code should be run automatically!
- example code should be run automatically!
- shell code should be run automatically!
- codeblocks are interpreted
- special considerations around server shutdown in the docs

GitHub Pages
````````````

Writing documentation
---------------------

Docstrings
``````````

- tenses, phrasing
- keep it brief
- document parameters, raises, returns

Tutorials
`````````

- structure of tutorials

Writing examples
----------------

- structure of examples

Supriya's examples live in :github-tree:`examples/`.

- use functions and classes because these play nicely with Sphinx' literalinclude

Inline code examples
````````````````````

- write the code examples externally to the restructuredtext
- use literalinclude to display the code in the documentation
- externalizing makes sure the code can be formatted, linted, typed, tested
