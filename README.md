# Supriya

[![](https://img.shields.io/pypi/pyversions/supriya)]()
[![](https://img.shields.io/pypi/l/supriya)]()
[![](https://img.shields.io/github/workflow/status/josiah-wolf-oberholtzer/supriya/Testing/master)]()

[Supriya](https://github.com/josiah-wolf-oberholtzer/supriya) is a
[Python](https://www.python.org/) API for
[SuperCollider](http://supercollider.github.io/).

Supriya lets you:

- Boot and communicate with SuperCollider's ``scsynth`` synthesis server in
  [realtime](http://josiahwolfoberholtzer.com/supriya/api/supriya/realtime/index.html)
- Compile
  [SynthDef](http://josiahwolfoberholtzer.com/supriya/api/supriya/synthdefs/index.html)s
natively in Python
- Explore non-realtime composition with object-oriented
  [Session](http://josiahwolfoberholtzer.com/supriya/api/supriya/nonrealtime/index.html)s
- Build realtime/non-realtime-agnostic,
  [asyncio](https://docs.python.org/3/library/asyncio.html)-aware applications
with
[Provider](http://josiahwolfoberholtzer.com/supriya/api/supriya/provider.html)s
- Schedule callbacks with tempo- and meter-aware
  [Clock](http://josiahwolfoberholtzer.com/supriya/api/supriya/clock/index.html)s
- Integrate with [IPython](http://ipython.org/),
  [Sphinx](https://www.sphinx-doc.org/en/master/) and
[Graphviz](http://graphviz.org/)

## Installation

Get [SuperCollider]() from [http://supercollider.github.io/](http://supercollider.github.io/).

Get Supriya from [PyPI]():

```bash
pip install supriya
```

... or from source:

```bash
git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
cd supriya/
pip install -e .
```

## Example: Hello World!

Let's make some noise. One synthesis context, one synth, one parameter change.

```
>>> import supriya
```

### Realtime

Grab a reference to the "default" realtime server and boot it:

```python
>>> server = supriya.Server.default().boot()
```

Add a synth, using the default `SynthDef`:

```python
>>> synth = server.add_synth()
```

Set the synth's frequency parameter like a dictionary:

```python
>>> synth["frequency"] = 123.45
```

Free the synth:

```python
>>> synth.free()
```

Quit the server:

```python
>>> server.quit()
```

### Non-realtime

Non-realtime work looks similar to realtime, with a couple key differences.

Create a `Session` instead of a `Server`:

```python
>>> session = supriya.Session()
```

Use `Session.at(...)` to select the desired point in time to make a mutation,
and add a synth using the default `SynthDef`, and an explicit duration for the
synth which the Session will use to terminate the synth automatically at the
appropriate timestep:

```python
>>> with session.at(0):
...     synth = session.add_synth(duration=2)
...
```

Select another point in time and modify the synth's frequency, just like in
realtime work:

```python
>>> with session.at(1):
...     synth["frequency"] = 123.45
...
```

Finally, render the session to disk:

```python
>>> session.render(duration=3)
(0, PosixPath('/Users/josiah/Library/Caches/supriya/session-981245bde945c7550fa5548c04fb47f7.aiff'))
```

## Example: Defining SynthDefs

Let's build a simple `SynthDef` for playing an audio buffer as a one-shot, with
panning and speed controls.

First, some imports, just to save horizontal space:

```python
>>> from supriya.ugens import Out, Pan2, PlayBuf
```

Second, define a builder with the control parameters we want for our `SynthDef`:

```python
>>> builder = supriya.SynthDefBuilder(amplitude=1, buffer_id=0, out=0, panning=0.0, rate=1.0)
```

Third, use the builder as a context manager. Unit generators defined inside the
context will be added automatically to the builder:

```python
>>> with builder:
...     player = PlayBuf.ar(
...         buffer_id=builder["buffer_id"],
...         done_action=supriya.DoneAction.FREE_SYNTH,
...         rate=builder["rate"],
...     )
...     panner = Pan2.ar(
...         source=player,
...         position=builder["panning"],
...         level=builder["amplitude"],
...     )
...     _ = Out.ar(bus=builder["out"], source=panner)
...
```

Finally, build the `SynthDef`, and print its structure. Supriya has given the
`SynthDef` a name automatically by hashing its structure:

```python
>>> synthdef = builder.build()
>>> print(synthdef)
synthdef:
    name: a056603c05d80c575333c2544abf0a05
    ugens:
    -   Control.kr: null
    -   PlayBuf.ar:
            buffer_id: Control.kr[1:buffer_id]
            done_action: 2.0
            loop: 0.0
            rate: Control.kr[4:rate]
            start_position: 0.0
            trigger: 1.0
    -   Pan2.ar:
            level: Control.kr[0:amplitude]
            position: Control.kr[3:panning]
            source: PlayBuf.ar[0]
    -   Out.ar:
            bus: Control.kr[2:out]
            source[0]: Pan2.ar[0]
            source[1]: Pan2.ar[1]
```

## Example: Playing Samples

Boot the server and allocate a sample:

```python
>>> server = supriya.Server.default().boot()
>>> buffer_ = server.add_buffer(
...     file_path="supriya/assets/audio/birds/birds-01.wav",
... )
>>> 
```

Allocate a synth using the `SynthDef` we defined before:

```
>>> synth = server.add_synth(synthdef=synthdef, buffer_id=buffer_)
```

The synth will play to completion and terminate itself.

## Example: Performing Patterns

Supriya implements a pattern library inspired by SuperCollider's, using nested
generators:

```python
from supriya.patterns import EventPattern, ParallelPattern, SequencePattern
pattern = ParallelPattern([
    EventPattern(
        frequency=SequencePattern([440, 550]),
    ),
    EventPattern(
        frequency=SequencePattern([1500, 1600, 1700]),
        delta=0.75,
    ),
])
```

Patterns can be manually iterated over:

```python
>>> for event in pattern:
...     event
... 
CompositeEvent([
    NoteEvent(UUID('ec648473-4e7b-4a9a-9708-6893c054ac0b'), delta=0.0, frequency=440),
    NoteEvent(UUID('32b84a7d-ba7b-4508-81f3-b9f560bc34a7'), delta=0.0, frequency=1500),
], delta=0.75)
NoteEvent(UUID('412f3bf3-df75-4eb5-bc9d-3e074bfd2f46'), delta=0.25, frequency=1600)
NoteEvent(UUID('69a01ba8-4c00-4b55-905a-99f3933a6963'), delta=0.5, frequency=550)
NoteEvent(UUID('2c6a6d95-f418-4613-b213-811a442ea4c8'), delta=0.5, frequency=1700)
```

Patterns can be played in real-time contexts:

```python
>>> server = supriya.Server().boot()
>>> _ = pattern.play(provider=server)
```

... or in non-realtime contexts:

```python
>>> session = supriya.Session()
>>> _ = pattern.play(provider=session, at=0.5)
>>> print(session.to_strings(include_controls=True))
0.0:
    NODE TREE 0 group
0.5:
    NODE TREE 0 group
        1001 default
            amplitude: 0.1, frequency: 1500.0, gate: 1.0, out: 0.0, pan: 0.5
        1000 default
            amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
2.0:
    NODE TREE 0 group
        1002 default
            amplitude: 0.1, frequency: 1600.0, gate: 1.0, out: 0.0, pan: 0.5
        1001 default
            amplitude: 0.1, frequency: 1500.0, gate: 1.0, out: 0.0, pan: 0.5
        1000 default
            amplitude: 0.1, frequency: 440.0, gate: 1.0, out: 0.0, pan: 0.5
2.5:
    NODE TREE 0 group
        1003 default
            amplitude: 0.1, frequency: 550.0, gate: 1.0, out: 0.0, pan: 0.5
        1002 default
            amplitude: 0.1, frequency: 1600.0, gate: 1.0, out: 0.0, pan: 0.5
3.5:
    NODE TREE 0 group
        1006 default
            amplitude: 0.1, frequency: 1700.0, gate: 1.0, out: 0.0, pan: 0.5
        1003 default
            amplitude: 0.1, frequency: 550.0, gate: 1.0, out: 0.0, pan: 0.5
        1002 default
            amplitude: 0.1, frequency: 1600.0, gate: 1.0, out: 0.0, pan: 0.5
4.0:
    NODE TREE 0 group
        1006 default
            amplitude: 0.1, frequency: 1700.0, gate: 1.0, out: 0.0, pan: 0.5
        1003 default
            amplitude: 0.1, frequency: 550.0, gate: 1.0, out: 0.0, pan: 0.5
4.5:
    NODE TREE 0 group
        1006 default
            amplitude: 0.1, frequency: 1700.0, gate: 1.0, out: 0.0, pan: 0.5
5.5:
    NODE TREE 0 group
```
