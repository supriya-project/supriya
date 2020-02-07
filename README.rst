supriya 0.1
===========

`Supriya`_ is a `Python`_ interface to `SuperCollider`_.

Supriya lets you:

-   boot and communicate with `SuperCollider`_'s ``scsynth`` synthesis server
-   construct and compile ``SynthDef`` unit generator graphs in native Python code
-   build and control graphs of synthesizers and synthesizer groups
-   object-model ``scysnth`` OSC communications explicitly via ``Request`` and
    ``Response`` classes
-   compile non-realtime synthesis scores via Supriya's
    ``nonrealtime.Session`` class

..  note:: This project is still under **heavy** development, is **not** yet
           stable, and is **not** yet intended for deployment in the field.

Send compliments or complaints to josiah.oberholtzer@gmail.com, or register
an issue at https://github.com/josiah-wolf-oberholtzer/supriya/issues.

Supriya is compatible with Python 3.6+ only.

..  image:: graph.png
    :align: center


`GitHub`_ |
`PyPI`_ |
`Documentation <http://supriya.mbrsi.org/>`_ |
`Issue Tracker <https://github.com/josiah-wolf-oberholtzer/supriya/issues>`_ |
`Mailing list <http://groups.google.com/group/supriya-dev>`_ |


Quickstart
----------

1. Get Supriya and SuperCollider
````````````````````````````````

Get Supriya from `GitHub`_::

    ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
    ~$ cd supriya
    supriya$ pip install -e .

Get `SuperCollider`_ from http://supercollider.github.io/.

Run the tests to make sure everything's OK::

    supriya$ pytest

Consult our installation instructions for detailed help on getting Supriya,
setting it up, and installing any additional dependencies like `Graphviz`_.


2. Make some noise
``````````````````

Start your Python interpreter and import Supriya::

    >>> import supriya

Boot the SuperCollider server::

    >>> server = supriya.Server.default()
    >>> server.boot()
    <Server: udp://127.0.0.1:57110, 8i8o>

Create and allocate a group::

    >>> group = supriya.realtime.Group().allocate()

Make a synthesizer definition and send it to the server::

    >>> builder = supriya.synthdefs.SynthDefBuilder(
    ...     amplitude=1.0,
    ...     frequency=440.0,
    ...     gate=1.0,
    ...     )

::

    >>> with builder:
    ...     source = supriya.ugens.SinOsc.ar(
    ...         frequency=builder['frequency'],
    ...         )
    ...     envelope = supriya.ugens.EnvGen.kr(
    ...         done_action=supriya.DoneAction.FREE_SYNTH,
    ...         envelope=supriya.synthdefs.Envelope.asr(),
    ...         gate=builder['gate'],
    ...         )
    ...     source = source * builder['amplitude']
    ...     source = source * envelope
    ...     out = supriya.ugens.Out.ar(
    ...         bus=0,
    ...         source=source,
    ...         )
    ...

::

    >>> synthdef = builder.build().allocate()

Synchronize with the server::

    >>> server.sync()
    <Server: udp://127.0.0.1:57110, 8i8o>

Create a synthesizer with the previously defined synthesizer definition::

    >>> synth = supriya.Synth(synthdef)
    >>> synth
    <Synth: ???>

Allocate it on the server as a child of the previously created group::

    >>> group.append(synth)
    >>> synth
    <Synth: 1001>

Query the server's node tree::

    >>> response = server.query_remote_nodes(include_controls=True)
    >>> print(response)
    NODE TREE 0 group
        1 group
            1000 group
                1001 f1c3ea5063065be20688f82b415c1108
                    amplitude: 0.0, frequency: 440.0

Release the synth::

    >>> synth.release()

Quit the server::

    >>> server.quit()
    <Server: offline>


..  _GitHub: https://github.com/josiah-wolf-oberholtzer/supriya
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _PyPI: https://pypi.python.org/pypi
..  _Python: https://www.python.org/
..  _SuperCollider: http://supercollider.github.io/
..  _Supriya: https://github.com/josiah-wolf-oberholtzer/supriya
..  _libsndfile: http://www.mega-nerd.com/libsndfile/
..  _pip: https://pip.pypa.io/en/stable/
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
..  _wavefile: https://pypi.python.org/pypi/wavefile/
