:hero: a Python API for SuperCollider

Supriya (|release|)
===================

.. attention::

   Documentation is under construction. Stand by.

:term:`Supriya` is a :term:`Python` API for :term:`SuperCollider`.

Supriya lets you:

- Boot and communicate with SuperCollider's ``scsynth``
  :py:mod:`~supriya.realtime.servers` synthesis engine in
  :py:mod:`~supriya.realtime`

- Compile SuperCollider :py:class:`SynthDefs
  <supriya.synthdefs.synthdefs.SynthDef>` natively in Python code

- Explore :py:mod:`~supriya.nonrealtime` composition with object-oriented
  :py:class:`sessions <supriya.nonrealtime.sessions.Session>`

- Build time-agnostic asyncio applications with
  :py:mod:`~supriya.providers`

- Schedule :py:mod:`~supriya.patterns` and callbacks with tempo- and
  meter-aware :py:mod:`~supriya.clocks`

- Integrate with `IPython`_, `Sphinx`_ and `Graphviz`_

Quickstart
----------

1. Get Supriya
``````````````

.. md-tab-set::

    .. md-tab-item:: From PyPI

        ::

            pip install supriya

    .. md-tab-item:: From source

        ::

            git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
            cd supriya
            pip install -e .

.. note::

    Consult our installation instructions for detailed help on getting Supriya,
    setting it up, and installing any additional dependencies like `Graphviz`_.

2. Get SuperCollider
````````````````````

Get `SuperCollider`_ from http://supercollider.github.io/.

3. Boot the server
``````````````````

Start your Python interpreter and import Supriya::

    >>> import supriya

Boot the SuperCollider server::

    >>> server = supriya.Server().boot()

3. Build a :term:`SynthDef`
```````````````````````````

Import some classes::

    >>> from supriya.ugens import EnvGen, Out, SinOsc
    >>> from supriya.synthdefs import Envelope, synthdef

Make a synthesizer definition::

    >>> @synthdef()
    ... def simple_sine(frequency=440, amplitude=0.1, gate=1):
    ...     sine = SinOsc.ar(frequency=frequency) * amplitude
    ...     envelope = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
    ...     Out.ar(bus=0, source=[sine * envelope] * 2)
    ...

Visualize the SynthDef (requires `Graphviz`_)::
    
    >>> supriya.graph(simple_sine)

Allocate it on the server::

    >>> _ = server.add_synthdef(simple_sine)

4. Create some nodes
````````````````````

Create and allocate a group::

    >>> group = server.add_group()

Synchronize with the server::

    >>> server.sync()

Create some synthesizers with the previously defined synthesizer definition, and
allocate them on the server as a child of the previously created group::

    >>> for i in range(3):
    ...     _ = group.add_synth(synthdef=simple_sine, frequency=111 * (i + 1))
    ...

Query the server's node tree::

    >>> print(server.query())

Visualize the server's node tree::

    >>> supriya.graph(server)

5. Release and quit
```````````````````

Release the synths::

    >>> for synth in group[:]:
    ...     synth.release()
    ...

Quit the server::

    >>> server.quit()

.. toctree::
    :caption: Getting Started
    :hidden:

    installation
    concepts

.. toctree::
    :caption: Tutorials
    :hidden:

    realtime/index
    nonrealtime/index
    osc
    synthdefs/index
    providers
    clocks
    patterns

.. toctree::
    :caption: How-to Guides
    :glob:
    :hidden:

    guides/*

.. toctree::
    :caption: API Reference
    :hidden:
    :maxdepth: 2

    api/supriya/index

.. toctree::
    :caption: Internals
    :glob:
    :hidden:

    internals/*


.. toctree::
    :caption: Appendix
    :hidden:

    glossary

..  _Cython: https://cython.org/
..  _GitHub: https://github.com/josiah-wolf-oberholtzer/supriya
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _IPython: https://ipython.org/
..  _PyPI: https://pypi.python.org/pypi
..  _Python: https://www.python.org/
..  _Sphinx: https://www.sphinx-doc.org/en/master/
..  _SuperCollider: http://supercollider.github.io/
..  _Supriya: https://github.com/josiah-wolf-oberholtzer/supriya
..  _libsndfile: http://www.mega-nerd.com/libsndfile/
..  _pip: https://pip.pypa.io/en/stable/
..  _python-rtmidi: https://github.com/SpotlightKid/python-rtmidi
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
..  _wavefile: https://pypi.python.org/pypi/wavefile/
