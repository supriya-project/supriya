.. _index:

Supriya |version|
=================

Supriya is a Python interface to SuperCollider.

Supriya lets you:

-   boot and communicate with SuperCollider's `scsynth` synthesis server
-   construct and compile `SynthDef` unit generator graphs in native Python code
-   build and control graphs of synthesizers and synthesizer groups
-   object-model `scysnth` OSC communications explicitly via `Request` and
    `Response` classes
-   schedule synthesizer events and patterns

Supriya's source is hosted at https://github.com/josiah-wolf-oberholtzer/supriya.

Documentation is available at http://supriya.readthedocs.org/en/latest/.

Join the development mailing list at supriya-dev@googlegroups.com.

..  note:: This project is still under **heavy** development, is **not** yet
           stable, and is **not** yet intended for deployment in the field.

Send compliments or complaints to josiah.oberholtzer@gmail.com, or register
an issue at https://github.com/josiah-wolf-oberholtzer/supriya/issues.

Compatible with Python 2.7, 3.3 and 3.4. 

Basta.

..  image:: graph.png
    :align: center

Installation
------------

To install, simply clone **supriya** and run the included `setup.py`:

::

    ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
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
- `six`
- `sphinx`
- `tornado`
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

    >>> from supriya import servertools
    >>> from supriya import synthdeftools
    >>> from supriya import ugentools

Boot the SuperCollider server:

    >>> server = servertools.Server()
    >>> server.boot()
    <Server: udp://127.0.0.1:57751, 8i8o>

Create and allocate a group:

    >>> group = servertools.Group().allocate()

Make a synthesizer definition and send it to the server:

    >>> builder = synthdeftools.SynthDefBuilder(
    ...     amplitude=1.0,
    ...     frequency=440.0,
    ...     gate=1.0,
    ...     )
    >>> with builder:
    ...     source = ugentools.SinOsc.ar(
    ...         frequency=builder['frequency'],
    ...         )
    ...     envelope = ugentools.EnvGen.kr(
    ...         done_action=synthdeftools.DoneAction.FREE_SYNTH,
    ...         envelope=synthdeftools.Envelope.asr(),
    ...         gate=builder['gate'],
    ...         )
    ...     source = source * builder['amplitude']
    ...     source = source * envelope
    ...     out = ugentools.Out.ar(
    ...         bus=(0, 1),
    ...         source=source,
    ...         )
    ...
    >>> synthdef = builder.build().allocate()

Synchronize with the server:

    >>> server.sync()
    <Server: udp://127.0.0.1:57751, 8i8o>

Create a synthesizer with the previously defined synthesizer definition:

    >>> synth = servertools.Synth(synthdef)
    >>> synth
    <Synth: ???>

Allocate it on the server as a child of the previously created group:

    >>> group.append(synth)
    >>> synth
    <Synth: 1001>

Query the server's node tree:

    >>> response = server.query_remote_nodes(include_controls=True)
    >>> print(response)
    NODE TREE 0 group
        1 group
            1000 group
                1001 f1c3ea5063065be20688f82b415c1108
                    amplitude: 0.0, frequency: 440.0

Bind a MIDI controller to the synth's controls:

    >>> korg = miditools.NanoKontrol2()
    >>> korg.open_port(0)
    >>> source = korg.fader_1
    >>> target = synth.controls['frequency']
    >>> bind(source, target, range_=Range(110, 880), exponent=2.0)
    Binding()

Release the synth:

    >>> synth.release()

Quit the server:

    >>> server.quit()
    <Server: offline>

About Supriya
-------------

..  toctree::
    :maxdepth: 2

    about/index

User Guide
----------

..  toctree::
    :maxdepth: 3

    users/index

Examples
--------

..  toctree::
    :maxdepth: 2

    examples/index

Supriya API
-----------

..  toctree::
    :maxdepth: 2

    api/index

Developer Guide
---------------

..  toctree::
    :maxdepth: 3

    developers/index

Indices and tables
==================
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`