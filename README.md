# Supriya

[![](https://img.shields.io/pypi/pyversions/supriya)]()
[![](https://img.shields.io/pypi/l/supriya)]()
[![](https://img.shields.io/github/workflow/status/josiah-wolf-oberholtzer/supriya/Testing/main)]()

[Supriya](https://github.com/josiah-wolf-oberholtzer/supriya) is a
[Python](https://www.python.org/) API for
[SuperCollider](http://supercollider.github.io/).

Supriya lets you:

- Boot and communicate with ``scsynth``
  [servers](http://josiahwolfoberholtzer.com/supriya/api/supriya/realtime/servers.html)
  in
  [realtime](http://josiahwolfoberholtzer.com/supriya/api/supriya/realtime/index.html)

- Compile
  [synth definitions](http://josiahwolfoberholtzer.com/supriya/api/supriya/synthdefs/index.html)
  natively in Python code

- Explore
  [nonrealtime](http://josiahwolfoberholtzer.com/supriya/api/supriya/nonrealtime/index.html)
  composition with object-oriented
  [sessions](http://josiahwolfoberholtzer.com/supriya/api/supriya/nonrealtime/index.html)

- Build time-agnostic
  [asyncio](https://docs.python.org/3/library/asyncio.html)-aware applications
  with
  [providers](http://josiahwolfoberholtzer.com/supriya/api/supriya/providers.html)

- Schedule
  [patterns](http://josiahwolfoberholtzer.com/supriya/api/supriya/patterns/index.html)
  and callbacks with tempo- and meter-aware
  [clocks](http://josiahwolfoberholtzer.com/supriya/api/supriya/clocks/index.html)

- Integrate with [IPython](http://ipython.org/),
  [Sphinx](https://www.sphinx-doc.org/en/master/) and
  [Graphviz](http://graphviz.org/)

## Installation

Get [SuperCollider]() from
[http://supercollider.github.io/](http://supercollider.github.io/).

Get Supriya from PyPI:

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

Grab a reference to a realtime server and boot it:

```python
>>> server = supriya.Server().boot()
```

Add a synth, using the default `SynthDef`:

```python
>>> synth = server.add_synth()
```

Set the synth's frequency parameter like a dictionary:

```python
>>> synth["frequency"] = 123.45
```

Release the synth:

```python
>>> synth.release()
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

Let's build a simple `SynthDef` for playing a sine tone with an ADSR envelope.

First, some imports:

```python
>>> from supriya.ugens import EnvGen, Out, SinOsc
>>> from supriya.synthdefs import Envelope, synthdef
```

We'll define a function and *decorate* it with the `synthdef` decorator:

```python
>>> @synthdef()
... def simple_sine(frequency=440, amplitude=0.1, gate=1):
...     sine = SinOsc.ar(frequency) * amplitude
...     envelope = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
...     Out.ar(0, [sine * envelope] * 2)
...
```

This results *not* in a function definition, but in the creation of a `SynthDef` object:

```python
>>> simple_sine
<SynthDef: simple_sine>
```

... which we can print to dump out its structure:

```python
>>> print(simple_sine)
synthdef:
    name: simple_sine
    ugens:
    -   Control.kr: null
    -   SinOsc.ar:
            frequency: Control.kr[1:frequency]
            phase: 0.0
    -   BinaryOpUGen(MULTIPLICATION).ar/0:
            left: SinOsc.ar[0]
            right: Control.kr[0:amplitude]
    -   EnvGen.kr:
            gate: Control.kr[2:gate]
            level_scale: 1.0
            level_bias: 0.0
            time_scale: 1.0
            done_action: 2.0
            envelope[0]: 0.0
            envelope[1]: 3.0
            envelope[2]: 2.0
            envelope[3]: -99.0
            envelope[4]: 1.0
            envelope[5]: 0.01
            envelope[6]: 5.0
            envelope[7]: -4.0
            envelope[8]: 0.5
            envelope[9]: 0.3
            envelope[10]: 5.0
            envelope[11]: -4.0
            envelope[12]: 0.0
            envelope[13]: 1.0
            envelope[14]: 5.0
            envelope[15]: -4.0
    -   BinaryOpUGen(MULTIPLICATION).ar/1:
            left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
            right: EnvGen.kr[0]
    -   Out.ar:
            bus: 0.0
            source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
```

Now let's boot the server:

```python
>>> server = supriya.Server().boot()
```

... add our `SynthDef` to it explicitly:

```python
>>> server.add_synthdef(simple_sine)
```

... make a synth using our new SynthDef:

```python
>>> synth = server.add_synth(simple_sine)
```

...release it:

```python
>>> synth.release()
```

...and quit:

```python
>>> server.quit()
```

## Example: SynthDef Builders

Let's build a simple `SynthDef` for playing an audio buffer as a one-shot, with
panning and speed controls.

This time we'll use Supriya's `SynthDefBuilder` context manager. It's more
verbose than decorating a function, but it also gives more flexibility. For
example, the context manager can be passed around from function to function to
add progressively more complexity. The `synthdef` decorator uses
`SynthDefBuilder` under the hood.

First, some imports, just to save horizontal space:

```python
>>> from supriya.ugens import Out, Pan2, PlayBuf
```

Second, define a builder with the control parameters we want for our
`SynthDef`:

```python
>>> builder = supriya.SynthDefBuilder(
...     amplitude=1, buffer_id=0, out=0, panning=0.0, rate=1.0
... )
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

Finally, build the `SynthDef`:


```python
>>> buffer_player = builder.build()
```

Let's print its structure. Note that Supriya has given the `SynthDef` a name
automatically by hashing its structure:

```python
>>> print(buffer_player)
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

"Anonymous" `SynthDef`s are great! Supriya keeps track of what `SynthDef`s have
been allocated by name, so naming them after the hash of their structure
guarantees no accidental overwrites and no accidental re-allocations.

## Example: Playing Samples

Boot the server and allocate a sample:

```python
>>> server = supriya.Server().boot()
>>> buffer_ = server.add_buffer(file_path="supriya/assets/audio/birds/birds-01.wav")
```

Allocate a synth using the `SynthDef` we defined before:

```
>>> server.add_synth(synthdef=buffer_player, buffer_id=buffer_)
<+ Synth: 1000 a056603c05d80c575333c2544abf0a05>
```

The synth will play to completion and terminate itself.

## Example: Performing Patterns

Supriya implements a pattern library inspired by SuperCollider's, using nested
generators.

Let's import some pattern classes:

```python
>>> from supriya.patterns import EventPattern, ParallelPattern, SequencePattern
```

... then define a pattern comprised of two *event* patterns played in parallel:

```
>>> pattern = ParallelPattern([
...     EventPattern(
...         frequency=SequencePattern([440, 550]),
...     ),
...     EventPattern(
...         frequency=SequencePattern([1500, 1600, 1700]),
...         delta=0.75,
...     ),
... ])
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

Patterns can be played (and stopped) in real-time contexts:

```python
>>> server = supriya.Server().boot()
>>> player = pattern.play(provider=server)
>>> player.stop()
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

## Example: Asyncio

Supriya also supports asyncio, with async servers, providers and clocks.

Async servers expose a minimal interface (effectively just `.boot()`, `.send()`
and `.quit()`), and don't support the rich stateful entities their non-async
siblings do (e.g. `Group`, `Synth`, `Bus`, `Buffer`). To split the difference,
we'll wrap the async server with a `Provider` that exposes an API of common
actions and returns lightweight stateless *proxies* we can use as references.
The proxies know their IDs and provide convenience functions, but otherwise
don't keep track of changes reported by the server.

Let's grab a couple imports:

```python
import asyncio, random
```

... and get a little silly.

First we'll define an async clock callback. It takes a `Provider` and a list of
buffer proxies created elsewhere by that provider, picks a random buffer and
uses the `buffer_player` `SynthDef` we defined earlier to play it (with a lot
of randomized parameters). Finally, it returns a random *delta* between 0 beats
and 2/4:


```python
async def callback(clock_context, provider, buffer_proxies):
    print("playing a bird...")
    buffer_proxy = random.choice(buffer_proxies)
    async with provider.at():
        provider.add_synth(
            synthdef=buffer_player,
            buffer_id=buffer_proxy,
            amplitude=random.random(),
            rate=random.random() * 2,
            panning=(random.random() * 2) - 1,
        )
    return random.random() * 0.5
```

Next we'll define our top-level async function. This one boots the server,
creates the `Provider` we'll use to interact with it, loads in all of Supriya's
built-in bird samples, schedules our clock callback with an async clock, waits
10 seconds and shuts down:

```python
async def serve():
    print("preparing the birds...")
    # Boot an async server
    server = await supriya.AsyncServer().boot(
        port=supriya.osc.utils.find_free_port(),
    )
    # Create a provider for higher-level interaction
    provider = supriya.Provider.from_context(server)
    # Use the provider as a context manager and load some buffers
    async with provider.at():
        buffer_proxies = [
            provider.add_buffer(file_path=bird_sample)
            for bird_sample in supriya.Assets["audio/birds/*"]
        ]
    # Create an async clock
    clock = supriya.AsyncClock()
    # Schedule our bird-playing clock callback to run immediately
    clock.schedule(callback, args=[provider, buffer_proxies])
    # Start the clock
    await clock.start()
    # Wait 10 seconds
    await asyncio.sleep(10)
    # Stop the clock
    await clock.stop()
    # And quit the server
    await server.quit()
    print("... done!")
```

Let's make some noise:

```python
>>> asyncio.run(serve())
preparing the birds...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
playing a bird...
... done!
```

Working async means we can hook into other interesting projects like
[python-prompt-toolkit](https://python-prompt-toolkit.readthedocs.io/),
[aiohttp](https://docs.aiohttp.org/) and
[pymonome](https://github.com/artfwo/pymonome).
