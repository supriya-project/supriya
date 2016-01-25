Installation
============

Supriya works on OSX and Unix/Linux with Python 3.3+.

Install Supriya
---------------

To install Supriya from its `GitHub`_ repository, via
`git <https://git-scm.com/>`_ and `pip`_::

    ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git 
    ~$ cd supriya
    supriya$ sudo pip install -e .

Install SuperCollider
`````````````````````

Install Graphviz (optional)
```````````````````````````

Development installation
------------------------

Virtual environments
--------------------

We strongly recommend installing Supriya into a virtual environment, especially
if you intend to hack on Supriya's own source code. Virtual environments allow
you to isolate `Python`_ packages from your systems global collection of
packages. They also allow you to install Python packages without ``sudo``. The
`virtualenv`_ package provides tools for creating Python virtual environments,
and the `virtualenvwrapper`_ package provides additional tools which make
working with virtual environments incredibly easy.

To install and setup `virtualenv`_ and `virtualenvwrapper`_::

    ~$ pip install virtualenvwrapper
    ...
    ~$ mkdir -p $WORKON_HOME
    ~$ export WORKON_HOME=~/.virtualenvs
    ~$ source /usr/local/bin/virtualenvwrapper.sh

Make the last two lines teaching your shell about the virtual environment
tools "sticky" by adding them to your profile::

    ~$ echo "export WORKON_HOME=~/.virtualenvs" >> ~/.profile
    ~$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
 
 With the virtual environment tools installed, create and activate a virtual
 environment. You can now install supriya into that environment::

    ~$ mkvirtualenv my-supriya-env
    ...
    (my-supriya-env) ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
    (my-supriya-env) ~$ cd supriya
    (my-supriya-env) supriya$ pip install -e ".[development]"

See the `virtualenvwrapper`_ documentation for instructions on how to use the
provided tools for working creating, deleting, activating and deactivating
virtual environments:`mkvirtualenv`, `rmvirtualenv`, `workon` and
`deactivate`.
