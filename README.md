supriya
=======

A Python interface to SuperCollider.

Example
-------

    >>> from supriya import servertools
    >>> server = servertools.Server()
    >>> server.boot()
    <Server: udp://127.0.0.1:57751, 8i8o>

    >>> group_a = servertools.Group().allocate()

    >>> from supriya import synthdeftools
    >>> from supriya import ugentools
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
    >>> synthdef.allocate()
    >>> server.sync()
    <Server: udp://127.0.0.1:57751, 8i8o>

    >>> synth = servertools.Synth(synthdef).allocate(
    ...     target_node=group_a,
    ...     )

    >>> response = server.query_remote_nodes(include_controls=True)
    >>> print(response)
    NODE TREE 0 group
        1 group
            1001 group
                1003 f1c3ea5063065be20688f82b415c1108
                    amplitude: 0.0, frequency: 440.0
            1000 group
                1002 group

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
- [ ] Implement complete Bus API
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

Distant Roadmap
---------------

- [ ] PySide-based GUI generation
- [ ] Kivy-based GUI generation
- [ ] Non-realtime composition
    - [ ] NRTScore
    - [ ] NRT node graph time slicing?

