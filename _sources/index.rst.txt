:hero: a Python API for SuperCollider

Supriya (|release|)
===================

:term:`Supriya` is a :term:`Python` API for :term:`SuperCollider`.

Supriya lets you:

- Boot and communicate with SuperCollider's synthesis engine in
  realtime.

- Explore :py:mod:`~supriya.contexts.nonrealtime` composition with 
  :py:class:`scores <supriya.contexts.nonrealtime.Score>`.

- Compile SuperCollider :py:class:`SynthDefs
  <supriya.ugens.bases.SynthDef>` natively in Python code.

- Build time-agnostic :py:mod:`asyncio`-aware applications with the
  :py:class:`context <supriya.contexts.core.Context>` interface.

- Schedule :py:mod:`~supriya.patterns` and callbacks with tempo- and
  meter-aware :py:mod:`~supriya.clocks`.

- Integrate with `IPython`_, `Sphinx`_ and `Graphviz`_.

Have fun!

| xoxo,
| `joséphine`_

Quickstart
----------

1. Get Supriya
``````````````

..  include:: /includes/install.txt

..  note::

    Consult our :doc:`installation instructions </introduction/installation>`
    for detailed help on getting Supriya, setting it up, and installing any
    additional dependencies like `Graphviz`_.

2. Get SuperCollider
````````````````````

Get `SuperCollider`_ from https://supercollider.github.io/.

3. Boot the server
``````````````````

Start your Python interpreter and import Supriya::

    >>> import supriya

Boot the SuperCollider server::

    >>> server = supriya.Server().boot()

4. Build a :term:`SynthDef`
```````````````````````````

Import some classes::

    >>> from supriya import Envelope, synthdef
    >>> from supriya.ugens import EnvGen, Out, SinOsc

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

    >>> _ = server.add_synthdefs(simple_sine)

... and then sync the server before proceeding to ensure the SynthDef has been
fully parsed by scsynth::

    >>> _ = server.sync()

5. Create some nodes
````````````````````

Create and allocate a group::

    >>> group = server.add_group()

Create some synthesizers with the previously defined synthesizer definition, and
allocate them on the server as a child of the previously created group::

    >>> for i in range(3):
    ...     _ = group.add_synth(simple_sine, frequency=111 * (i + 1))
    ...

Query the server's node tree::

    >>> print(server.query_tree())

6. Release and quit
```````````````````

Release the synths::

    >>> for synth in group.children[:]:
    ...     synth.free()
    ...

Quit the server::

    >>> server.quit()

..  toctree::
    :caption: Introduction
    :hidden: 

    introduction/installation
    introduction/history.rst
    introduction/concepts.rst

..  toctree::
    :caption: Core tutorials
    :hidden: 

    tutorials/index
    tutorials/contexts
    tutorials/servers
    tutorials/nodes
    tutorials/buses
    tutorials/buffers
    tutorials/synthdefs
    tutorials/osc
    tutorials/scores

..  toctree::
    :caption: Advanced tutorials
    :hidden: 

    advanced/index
    advanced/clocks
    advanced/patterns
    advanced/extensions

..  toctree::
    :caption: Examples
    :hidden: 

    examples/index
    examples/hello_world
    examples/hello_world_contexts
    examples/hello_world_debugged

..  toctree::
    :caption: For developers
    :hidden: 

    developers/index
    developers/testing
    developers/documenting
    developers/releasing

..  toctree::
    :caption: API Reference
    :hidden: 
    :maxdepth: 2

    api/supriya/index

..  toctree::
    :hidden: 
    :caption: Appendices

    appendices/glossary
