#!/usr/bin/env python

import sys
from distutils.core import setup
from distutils.version import StrictVersion

install_requires = [
    'abjad',
    'numpy',
    'pexpect',
    'pytest',
    'rtmidi-python',
    'sphinx',
    'sphinx_rtd_theme',
    'tox',
    'wavefile',
    ]
version = '.'.join(str(x) for x in sys.version_info[:3])
if StrictVersion(version) < StrictVersion('3.4.0'):
    install_requires.append('enum34')
if StrictVersion(version) < StrictVersion('3.3.0'):
    install_requires.append('funcsigs')

long_description = '''
supriya
=======

A Python interface to SuperCollider.

Supriya lets you:

-   boot and communicate with SuperCollider's `scsynth` synthesis server
-   construct and compile `SynthDef` unit generator graphs in native Python code
-   build and control graphs of synthesizers and synthesizer groups
-   object-model `scysnth` OSC communications explicitly via `Request` and
    `Response` classes
-   schedule synthesizer events and patterns

Documentation is available at http://supriya.readthedocs.org/en/latest/.

Please note: this project is still under **heavy** development, is **not** yet
stable, and is **not** yet intended for deployment in the field.

Send compliments or complaints to josiah.oberholtzer@gmail.com, or register
an issue at https://github.com/Pulgama/supriya/issues.

Compatible with Python 2.7, 3.3 and 3.4.

Basta.

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
- `wavefile`
- `rtmidi-python`
- `sphinx_rtd_theme`
- `sphinx`
- `tox`

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

Current Roadmap
---------------

- [X] Cleanup server object proxies
    - [X] BufferGroup, Buffer, BufferProxy
    - [X] BusGroup, Bus, BusProxy (for both Audio and Control buses)
    - [X] SynthControl
        - [X] QueryTreeControl.from_control()
- [X] Make SynthDef immutable
    - [X] Implement SynthDefBuilder
    - [X] Implement Parameter class (model a single control name, value, rate)
    - [X] Implement AudioControl and TrigControl UGens
- [ ] Explicitly object model Server requests
    - [ ] Audit all asynchronous request/response pairs
- [X] Implement complete Buffer API
    - [X] `/b_alloc`
    - [X] `/b_allocRead`, `/b_allocReadChannel`
    - [X] `/b_read`, `/b_readChannel`
    - [X] `/b_write`, `/b_close`
    - [X] `/b_get`, `/b_getn`
    - [X] `/b_set`, `/b_setn`
    - [X] `/b_query`
    - [X] `/b_gen`, `/b_fill`, `/b_zero`
    - [X] `/b_free`
- [ ] Implement complete Bus(-related) API
    - [ ] `/c_set`, `/c_setn`
    - [ ] `/c_fill`
    - [ ] `/c_get`, `/c_getn`
    - [ ] `/n_map`, `/n_mapn`
    - [ ] `/n_mapa`, `/n_mapan`
- [ ] Implement all UGen binary operators
- [ ] Implement all UGen unary operators
- [ ] MIDI callbacks
- [ ] Port all UGens
    - [X] AudioIn.sc
    - [ ] BasicOpsUGen.sc
    - [ ] BEQSuite.sc
    - [ ] BufIO.sc
    - [ ] Chaos.sc
    - [ ] CheckBadValues.sc
    - [ ] Compander.sc
    - [X] Delays.sc
    - [ ] DelayWr.sc
    - [ ] Demand.sc
    - [ ] DiskIO.sc
    - [ ] EnvGen.sc
    - [ ] FFT.sc
    - [ ] Filter.sc
    - [ ] FreeVerb.sc
    - [ ] FSinOsc.sc
    - [ ] Gendyn.sc
    - [ ] GrainUGens.sc
    - [ ] GVerb.sc
    - [ ] Hilbert.sc
    - [X] InfoUGens.sc
    - [ ] InOut.sc
    - [ ] Line.sc
    - [ ] MachineListening.sc
    - [ ] MacUGens.sc
    - [ ] Mix.sc
    - [ ] MoogFF.sc
    - [ ] Noise.sc
    - [ ] Osc.sc
    - [ ] Pan.sc
    - [ ] PhysicalModel.sc
    - [X] PitchShift.sc
    - [ ] Pluck.sc
    - [ ] Poll.sc
    - [ ] PSinGraph.sc
    - [ ] Splay.sc
    - [ ] Trig.sc
    - [ ] UGen.sc
- [ ] Implement appropriate UGen input checking
- [ ] Port all UGen examples
- [ ] Write SynthDef compilation/sending tests to scsynth for all UGens
- [ ] Implement tempo-accurate clocks and scheduled OSCBundle logic

Distant Roadmap
---------------

- [ ] PySide-based GUI generation
- [ ] Kivy-based GUI generation
- [ ] Non-realtime composition
    - [ ] NRTScore
    - [ ] NRT node graph time slicing?

'''

entry_points = {
    'console_scripts': [
        'supriya = supriya.tools.systemtools.run_supriya:run_supriya'
        ],
    }

def main():
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        description='A Python API for SuperCollider',
        entry_points=entry_points,
        install_requires=install_requires,
        license='GPL',
        long_description=long_description,
        name='supriya',
        packages=('supriya',),
        url='https://github.com/Pulgama/supriya',
        version='0.1',
        zip_safe=False,
        )


if __name__ == '__main__':
    main()