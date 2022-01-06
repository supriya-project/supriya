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

    ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git 
    ~$ cd supriya
    supriya$ pip install -e .

Optional dependencies
---------------------

With `IPython`_ support::

    supriya$ pip install -e .[ipython]

With test dependencies::

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

Virtual environments
--------------------

We strongly recommend installing Supriya into a virtual environment, especially
if you intend to hack on Supriya's own source code. Virtual environments allow
you to isolate `Python`_ packages from your systems global collection of
packages. They also allow you to install Python packages without ``sudo``. The
`virtualenv`_ package provides tools for creating Python virtual environments,
and the `virtualenvwrapper`_ package provides additional tools which make
working with virtual environments incredibly easy.

To install and setup `virtualenv`_ and `virtualenvwrapper`_:

::

    ~$ pip install virtualenvwrapper
    ...
    ~$ mkdir -p $WORKON_HOME
    ~$ export WORKON_HOME=~/.virtualenvs
    ~$ source /usr/local/bin/virtualenvwrapper.sh

Make the last two lines teaching your shell about the virtual environment
tools "sticky" by adding them to your profile:

::

    ~$ echo "export WORKON_HOME=~/.virtualenvs" >> ~/.profile
    ~$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
 
With the virtual environment tools installed, create and activate a virtual
environment. You can now install supriya into that environment:

::

    ~$ mkvirtualenv my-supriya-env
    ...
    (my-supriya-env) ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
    (my-supriya-env) ~$ cd supriya
    (my-supriya-env) supriya$ pip install -e ".[development]"

See the `virtualenvwrapper`_ documentation for instructions on how to use the
provided tools for working creating, deleting, activating and deactivating
virtual environments: ``mkvirtualenv``, ``rmvirtualenv``, ``workon`` and
``deactivate``.

..  _Cython: https://cython.org/
..  _GitHub: https://github.com/josiah-wolf-oberholtzer/supriya
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _IPython: https://ipython.org/
..  _PyPI: https://pypi.python.org/pypi
..  _Python: https://www.python.org/
..  _SuperCollider: http://supercollider.github.io/
..  _Supriya: https://github.com/josiah-wolf-oberholtzer/supriya
..  _pip: https://pip.pypa.io/en/stable/
..  _python-rtmidi: https://github.com/SpotlightKid/python-rtmidi
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
