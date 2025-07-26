Installation
============

Get SuperCollider
-----------------

Supriya uses `SuperCollider`_ as its synthesis engine. `SuperCollider`_ is
available on OSX, Linux and Windows.

You can download `SuperCollider`_ from http://supercollider.github.io/.

Get Supriya
-----------

Install Supriya from `PyPI`_ via `pip`_, or from its `GitHub`_ repository via `git
<https://git-scm.com/>`_ and `pip`_:

.. include:: /includes/install.txt

Optional dependencies
---------------------

With `Sphinx`_ and `IPython`_ support:

.. include:: /includes/install-docs.txt

With linting and testing dependencies:

.. include:: /includes/install-test.txt

Graphviz
````````

Supriya uses `Graphviz`_, an open-source graph visualization library, to create
graphs of rhythm-trees and other tree structures, and to create visualizations
of class hierarchies for its documentation. Graphviz is not necessary for
making sounds with Supriya.

To install `Graphviz`_:

.. md-tab-set::

    .. md-tab-item:: OSX 

        Via `Homebrew`_:

        ::

            ~$ brew install graphviz

    .. md-tab-item:: Ubuntu

        Via ``apt``:

        ::

            ~$ sudo apt-get install graphviz

    .. md-tab-item:: Windows

        Via `Chocolatey`_:

        ::

            ~$ choco install graphviz

Once you have install `Graphviz`_, test if `Graphviz`_ is callable from your
command-line by running the following command:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.38.0 (20140413.2041)

FFmpeg and LAME
```````````````

Supriya's integrations with `IPython`_ and `Sphinx`_ need to ensure audio files
are websafe. To do this, Supriya uses `FFmpeg` and `LAME` to transcode audio
output from `SuperCollider`_ into OGG or MP3 files suitable for use in web
browsers. If you want to build Supriya's documentation or use Supriya in
Jupyter notebooks, make sure to install them:

.. md-tab-set::

    .. md-tab-item:: OSX 

        Via `Homebrew`_:

        ::

            ~$ brew install ffmpeg lame

    .. md-tab-item:: Ubuntu

        Via ``apt``:

        ::

            ~$ sudo apt-get install ffmpeg lame

    .. md-tab-item:: Windows

        Via `Chocolatey`_:

        ::

            ~$ choco install ffmpeg lame
