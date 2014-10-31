.. _index:

Supriya |version|
=================

..  image:: https://readthedocs.org/projects/supriya/badge/?version=latest
    :target: https://readthedocs.org/projects/supriya/?badge=latest
    :alt: Documentation Status

Supriya is a Python interface to SuperCollider.

Supriya lets you:

-   boot and communicate with SuperCollider's `scsynth` synthesis server
-   construct and compile `SynthDef` unit generator graphs in native Python code
-   build and control graphs of synthesizers and synthesizer groups
-   object-model `scysnth` OSC communications explicitly via `Request` and
    `Response` classes
-   schedule synthesizer events and patterns

Documentation is available at http://supriya.readthedocs.org/en/latest/.

..  note:: This project is still under **heavy** development, is **not** yet
           stable, and is **not** yet intended for deployment in the field.

Send compliments or complaints to josiah.oberholtzer@gmail.com, or register
an issue at https://github.com/Pulgama/supriya/issues.

Compatible with Python 2.7, 3.3 and 3.4. 

Basta.

..  image:: graph.png
    :align: center

Installation
------------

To install, simply clone **supriya** and run the included `setup.py`:

::

    ~$ git clone https://github.com/Pulgama/supriya.git
    ~$ cd supriya
    supriya$ sudo python setup.py install

To run the test suite:

::

    supriya$ tox 

Dependencies
------------

Make sure that SuperCollider is installed, and that `scsynth` is available from
the command-line. **supriya** targets SuperCollider 3.6.5 and above, although
it may work with earlier versions as well.

::

    ~$ scsynth -h
    supercollider_synth  options:
    ...

SuperCollider may be found at http://supercollider.sourceforge.net/ for all
platforms. Alternatively, many Linux distributions will allow you to install
SuperCollider via their package manager.

**supriya** has the following Python dependencies for all Python versions:

- `abjad`
- `numpy`
- `pexpect`
- `pytest`
- `rtmidi-python`
- `sphinx`
- `tox`
- `python-wavefile`

Additionally, **supriya** requires `funcsigs` with Python 2.7, and `enum34` for
both Python 2.7 and Python 3.3.

`python-wavefile` requires that `libsndfile` be installed. Source for
`libsndfile` for OSX platforms may be found at
http://www.mega-nerd.com/libsndfile/#Download.

When installed via the included `setup.py` file (`sudo python setup.py
install`) all of the above dependencies will be installed automatically.

**supriya** has not been tested with Python 3.x versions earlier than 3.3.

Example
-------

Import packages from **supriya**:

::

    >>> from supriya import servertools
    >>> from supriya import synthdeftools
    >>> from supriya import ugentools

Boot the SuperCollider server:

::

    >>> server = servertools.Server()
    >>> server.boot()
    <Server: udp://127.0.0.1:57751, 8i8o>

Create and allocate a group:

::

    >>> group = servertools.Group().allocate()

Make a synthesizer definition and send it to the server:

::

    >>> synthdef_builder = synthdeftools.SynthDefBuilder(
    ...     amplitude=0.0,
    ...     frequency=440.0,
    ...     )
    >>> sin_osc = ugentools.SinOsc.ar(
    ...     frequency=synthdef_builder['frequency'],
    ...     )
    >>> sin_osc *= synthdef_builder['amplitude']
    >>> out = ugentools.Out.ar(
    ...     bus=(0, 1),
    ...     source=sin_osc,
    ...     )
    >>> synthdef_builder.add_ugen(out)
    >>> synthdef = synthdef_builder.build().allocate(sync=True)

Synchronize with the server:

::

    >>> server.sync()
    <Server: udp://127.0.0.1:57751, 8i8o>

Create a synthesizer with the previously defined synthesizer definition, and
allocate it on the server as a child of the previously created group:

::

    >>> synth = servertools.Synth(synthdef)
    >>> synth.allocate(target_node=group)
    <Synth: 1001>

Query the server's node tree:

::

    >>> response = server.query_remote_nodes(include_controls=True)
    >>> print(response)
    NODE TREE 0 group
        1 group
            1000 group
                1001 f1c3ea5063065be20688f82b415c1108
                    amplitude: 0.0, frequency: 440.0

Quit the server:

::

    >>> server.quit()
    <Server: offline>

API Documentation
-----------------

..  toctree::
    :maxdepth: 2

    tools/index

Indices and tables
==================
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`