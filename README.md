supriya
=======

A Python interface to SuperCollider (very much in progress).

Current operative functionality:

- starting the SuperCollider server
- OSC communication to and from the server
- compiling synthesizer definitions identically to how SC would

Current Roadmap
---------------

[ ] Cleanup server object proxies
    [ ] BusGroup
    [ ] BufferGroup
    [ ] SynthControl
        [ ] QueryTreeControl.from_control()
[ ] Make SynthDef immutable
    [ ] Implement SynthDefBuilder
    [ ] Implement SynthDefControls aggregate
    [ ] Implement Control class (model a single control name, value, rate)
    [ ] Implement AudioControls and TriggerControls UGens
[ ] Implement complete Buffer API
[ ] Implement complete Bus API
    [ ] /c_set, /c_setn 
    [ ] /c_fill
    [ ] /c_get, /c_getn
    [ ] /n_map, /n_mapn
    [ ] /n_mapa, /n_mapan
[ ] MIDI callbacks
[ ] Port all UGens
    [ ] AudioIn.sc
    [ ] BasicOpsUGen.sc
    [ ] BEQSuite.sc
    [ ] BufIO.sc
    [ ] Chaos.sc
    [ ] CheckBadValues.sc
    [ ] Compander.sc
    [x] Delays.sc
    [ ] DelayWr.sc
    [ ] Demand.sc
    [ ] DiskIO.sc
    [ ] EnvGen.sc
    [ ] FFT.sc
    [ ] Filter.sc
    [ ] FreeVerb.sc
    [ ] FSinOsc.sc
    [ ] Gendyn.sc
    [ ] GrainUGens.sc
    [ ] GVerb.sc
    [ ] Hilbert.sc
    [x] InfoUGens.sc
    [ ] InOut.sc
    [ ] Line.sc
    [ ] MachineListening.sc
    [ ] MacUGens.sc
    [ ] Mix.sc
    [ ] MoogFF.sc
    [ ] Noise.sc
    [ ] Osc.sc
    [ ] Pan.sc
    [ ] PhysicalModel.sc
    [ ] PitchShift.sc
    [ ] Pluck.sc
    [ ] Poll.sc
    [ ] PSinGraph.sc
    [ ] Splay.sc
    [ ] Trig.sc
    [ ] UGen.sc

Distant Roadmap
---------------

[ ] PySide-based GUI generation
[ ] Kivy-based GUI generation
[ ] Non-realtime composition
    [ ] NRTScore
    [ ] NRT node graph time slicing?

