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

Make sure that SuperCollider is installed, and that `scsynth` is available from
the command-line.

Python dependencies for all Python versions:

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
    - [X] BufferGroup, Buffer, BufferProxy
    - [X] BusGroup, Bus, BusProxy (for both Audio and Control buses)
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
- [ ] Implement all UGen binary operators
    - [X] `ADD = 0`
    - [X] `SUB = 1`
    - [X] `MUL = 2`
    - [X] `IDIV = 3`
    - [X] `FDIV = 4`
    - [X] `MOD = 5`
    - [ ] `EQ = 6`
    - [ ] `NE = 7`
    - [ ] `LT = 8`
    - [ ] `GT = 9`
    - [ ] `LE = 10`
    - [ ] `GE = 11`
    - [ ] `MIN = 12`
    - [ ] `MAX = 13`
    - [ ] `BIT_AND = 14`
    - [ ] `BIT_OR = 15`
    - [ ] `BIT_XOR = 16`
    - [ ] `LCM = 17`
    - [ ] `GCD = 18`
    - [ ] `ROUND = 19`
    - [ ] `ROUND_UP = 20`
    - [ ] `TRUNC = 21`
    - [ ] `ATAN2 = 22`
    - [ ] `HYPOT = 23`
    - [ ] `HYPOTX = 24`
    - [ ] `POW = 25`
    - [ ] `SHIFT_LEFT = 26`
    - [ ] `SHIFT_RIGHT = 27`
    - [ ] `UNSIGNED_SHIFT = 28`
    - [ ] `FILL = 29`
    - [ ] `RING1 = 30  # a * (b + 1) == a * b + a`
    - [ ] `RING2 = 31  # a * b + a + b`
    - [ ] `RING3 = 32  # a*a*b`
    - [ ] `RING4 = 33  # a*a*b - a*b*b`
    - [ ] `DIFFERENCE_OF_SQUARES = 34  # a*a - b*b`
    - [ ] `SUM_OF_SQUARES = 35  # a*a + b*b`
    - [ ] `SQUARE_OF_SUM = 36  # (a + b)^2`
    - [ ] `SQUARE_OF_DIFFERENCE = 37  # (a - b)^2`
    - [ ] `ABSDIFF = 38  # |a - b|`
    - [ ] `THRESH = 39`
    - [ ] `AMCLIP = 40`
    - [ ] `SCALE_NEG = 41`
    - [ ] `CLIP2 = 42`
    - [ ] `EXCESS = 43`
    - [ ] `FOLD2 = 44`
    - [ ] `WRAP2 = 45`
    - [ ] `FIRST_ARG = 46`
    - [ ] `RANDRANGE = 47`
    - [ ] `EXPRANDRANGE = 48`
- [ ] Implement all UGen unary operators
    - [X] `NEG = 0`
    - [ ] `NOT = 1`
    - [ ] `IS_NIL = 2`
    - [ ] `NOT_NIL = 3`
    - [ ] `BIT_NOT = 4`
    - [ ] `ABS = 5`
    - [ ] `AS_FLOAT = 6`
    - [ ] `AS_INT = 7`
    - [ ] `CEIL = 8`
    - [ ] `FLOOR = 9`
    - [ ] `FRACTION = 10`
    - [ ] `SIGN = 11`
    - [ ] `SQUARED = 12`
    - [ ] `CUBED = 13`
    - [ ] `SQRT = 14`
    - [ ] `EXP = 15`
    - [ ] `RECIPROCAL = 16`
    - [ ] `MIDI_TO_FREQ = 17`
    - [ ] `FREQ_TO_MIDI = 18`
    - [ ] `MIDI_TO_RATIO = 19`
    - [ ] `RATIO_TO_MIDI = 20`
    - [ ] `DB_TO_AMP = 21`
    - [ ] `AMP_TO_DB = 22`
    - [ ] `OCTAVE_TO_FREQ = 23`
    - [ ] `FREQ_TO_OCTAVE = 24`
    - [ ] `LOG = 25`
    - [ ] `LOG2 = 26`
    - [ ] `LOG10 = 27`
    - [ ] `SIN = 28`
    - [ ] `COS = 29`
    - [ ] `TAN = 30`
    - [ ] `ARCSIN = 31`
    - [ ] `ARCCOS = 32`
    - [ ] `ARCTAN = 33`
    - [ ] `SINH = 34`
    - [ ] `COSH = 35`
    - [ ] `TANH = 36`
    - [ ] `RAND = 37`
    - [ ] `RAND2 = 38`
    - [ ] `LINRAND = 39`
    - [ ] `BILINRAND = 40`
    - [ ] `SUM3RAND = 41`
    - [ ] `DISTORT = 42`
    - [ ] `SOFTCLIP = 43`
    - [ ] `COIN = 44`
    - [ ] `DIGIT_VALUE = 45`
    - [ ] `SILENCE = 46`
    - [ ] `THRU = 47`
    - [ ] `RECTANGLE_WINDOW = 48`
    - [ ] `HANNING_WINDOW = 49`
    - [ ] `WELCH_WINDOW = 50`
    - [ ] `TRIANGLE_WINDOW = 51`
    - [ ] `RAMP = 52`
    - [ ] `SCURVE = 53`
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

Distant Roadmap
---------------

- [ ] PySide-based GUI generation
- [ ] Kivy-based GUI generation
- [ ] Non-realtime composition
    - [ ] NRTScore
    - [ ] NRT node graph time slicing?

