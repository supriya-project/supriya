supriya
=======

A Python interface to SuperCollider.

Tested and compatible with Python 2.7, 3.3 and 3.4.

Installation
------------

To install, simply clone **supriya** and run the included `setup.py`:

    ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
    ~$ cd supriya
    supriya$ sudo python setup.py install

To run the test suite:

    supriya$ tox 

Dependencies
------------

For all Python versions:

- abjad
- pexpect
- pytest
- rtmidi-python
- sphinx
- tox

On Python 2.7:

- funcsigs
- enum34

On Python 3.3:

- enum34

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

Make a synthesizer definition:

    >>> synthdef = synthdeftools.SynthDef(
    ...     amplitude=0.0,
    ...     frequency=440.0,
    ...     )
    >>> controls = synthdef.controls
    >>> sin_osc = ugentools.SinOsc.ar(
    ...     frequency=controls['frequency'],
    ...     )
    >>> sin_osc *= controls['amplitude']
    >>> out = ugentools.Out.ar(
    ...     bus=(0, 1),
    ...     source=sin_osc,
    ...     )
    >>> synthdef.add_ugen(out)

Send the synthesizer definition to the server:

    >>> synthdef.allocate()

Synchronize with the server:

    >>> server.sync()
    <Server: udp://127.0.0.1:57751, 8i8o>

Create a synthesizer with the previously defined synthesizer definition, and
allocate it on the server as a child of the previously created group:

    >>> synth = servertools.Synth(synthdef).allocate(
    ...     target_node=group,
    ...     )

Query the server's node tree:

    >>> response = server.query_remote_nodes(include_controls=True)
    >>> print(response)
    NODE TREE 0 group
        1 group
            1001 group
                1003 f1c3ea5063065be20688f82b415c1108
                    amplitude: 0.0, frequency: 440.0
            1000 group
                1002 group

Quit the server:

    >>> server.quit()
    <Server: offline>

Current Roadmap
---------------

- [ ] Cleanup server object proxies
    - [ ] BusGroup
    - [ ] BufferGroup
    - [ ] SynthControl
        - [ ] QueryTreeControl.from_control()
- [ ] Make SynthDef immutable
    - [ ] Implement SynthDefBuilder
    - [ ] Implement SynthDefControls aggregate
    - [ ] Implement Control class (model a single control name, value, rate)
    - [ ] Implement AudioControls and TriggerControls UGens
- [ ] Implement complete Buffer API
    - [ ] `/b_alloc`
    - [ ] `/b_allocRead`, `/b_allocReadChannel`
    - [ ] `/b_read`, `/b_readChannel`
    - [ ] `/b_write`, `/b_close`
    - [ ] `/b_get`, `/b_getn`
    - [ ] `/b_set`, `/b_setn`
    - [ ] `/b_query`
    - [ ] `/b_gen`, `/b_fill`, `/b_zero`
    - [ ] `/b_free`
- [ ] Implement complete Bus(-related) API
    - [ ] `/c_set`, `/c_setn `
    - [ ] `/c_fill`
    - [ ] `/c_get`, `/c_getn`
    - [ ] `/n_map`, `/n_mapn`
    - [ ] `/n_mapa`, `/n_mapan`
- [ ] MIDI callbacks
- [ ] Port all UGens
    - [ ] AudioIn.sc
    - [ ] BasicOpsUGen.sc
    - [ ] BEQSuite.sc
    - [ ] BufIO.sc
    - [ ] Chaos.sc
    - [ ] CheckBadValues.sc
    - [ ] Compander.sc
    - [x] Delays.sc
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
    - [x] InfoUGens.sc
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
    - [ ] PitchShift.sc
    - [ ] Pluck.sc
    - [ ] Poll.sc
    - [ ] PSinGraph.sc
    - [ ] Splay.sc
    - [ ] Trig.sc
    - [ ] UGen.sc
- [ ] Implement appropriate UGen input checking
- [ ] Port all UGen examples
- [ ] Write SynthDef compilation/sending tests to scsynth for all UGens

Distant Roadmap
---------------

- [ ] PySide-based GUI generation
- [ ] Kivy-based GUI generation
- [ ] Non-realtime composition
    - [ ] NRTScore
    - [ ] NRT node graph time slicing?

