Installation
============

Get SuperCollider
-----------------

Supriya uses `SuperCollider`_ as its synthesis engine. `SuperCollider`_ is
available on OSX, Linux and Windows (although Supriya has not been tested on
Windows).

You can download `SuperCollider`_ from http://supercollider.github.io/.

Get Supriya
-----------

Install Supriya from its `GitHub`_ repository, via `git
<https://git-scm.com/>`_ and `pip`_::

    ~$ git clone https://github.com/supriya-project/supriya.git 
    ~$ cd supriya
    supriya$ pip install -e .

Optional dependencies
---------------------

With `Sphinx`_ and `IPython`_ support::

    supriya$ pip install -e .[docs]

With linting and testing dependencies::

    supriya$ pip install -e .[test]

Graphviz
````````

Supriya uses `Graphviz`_, an open-source graph visualization library, to create
graphs of rhythm-trees and other tree structures, and to create visualizations
of class hierarchies for its documentation. Graphviz is not necessary for
making sounds with Supriya.

To install `Graphviz`_ on Debian and Ubuntu::

    ~$ sudo apt-get install graphviz

To install `Graphviz`_ on OSX via `Homebrew`_::

    ~$ brew install graphviz

Once you have install `Graphviz`_, test if `Graphviz`_ is callable from your
command-line by running the following command:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.38.0 (20140413.2041)

..  _Cython: https://cython.org/
..  _GitHub: https://github.com/supriya-project/supriya
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _IPython: https://ipython.org/
..  _PyPI: https://pypi.python.org/pypi
..  _Python: https://www.python.org/
..  _Sphinx: https://www.sphinx-doc.org/
..  _SuperCollider: http://supercollider.github.io/
..  _Supriya: https://github.com/supriya-project/supriya
..  _pip: https://pip.pypa.io/en/stable/
..  _python-rtmidi: https://github.com/SpotlightKid/python-rtmidi
