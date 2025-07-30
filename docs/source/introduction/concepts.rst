Core Concepts
=============

Supriya's documentation and code assumes that you have some familiarity with
the core concepts underpinning working with `SuperCollider`_, and working in
digital signal processing environments in general. Very little of what follows
in the documentation will make sense until you develop a good grasp of these
concepts.

Client and server
-----------------

`SuperCollider`_ is a collection of tools working in concert together.

The most important of these are the *client* (``sclang``) and the *server*
(``scsynth`` and ``supernova``).

The *server* produces audio as an output, potentially using audio as an input.
Like many other kinds of servers, ``scsynth`` listens for messages from
clients, takes actions based on those messages, and potentially sends messages
back to the *client* (or *clients*).

The *client* orchestrates what messages are sent to the *server* towards some
(usually musical) end. IT controls what commands are sent, and
- *importantly* - when they are sent. The client may take action based on
messages sent back by the server, but is not responsible for generating the
audio itself.

SuperCollider's client `sclang` is its own programming language with standard
library affordances for communicating with the SuperCollider server. Similarly,
Supriya is, as a client, a set of library affordances for communicating with
the SuperCollider server via `Python`_, and leans on the rest of the Python
ecosystem to fill in the gaps that ``sclang`` has to build from scratch (e.g.
packaging, documentation tooling, testing, scientific computing, UIs, etc.).

There are many non-``sclang`` clients beyond Supriya for a wide variety of
languages, but all follow the very broad pattern of orchestrating
communications with a running ``scsynth`` or ``supernova`` server. Most client,
including Supriya and ``sclang``, provide a class (or the equivalent in that
language) to model the concept of a server. In both Supriya and ``sclang`` this
class is called, unsurprisingly, :py:class:`~supriya.contexts.realtime.Server`
! However, this isn't actually the server, just a *proxy* to it as a
convenience for communications and process management.

Because of the communication and memory boundaries between the client and the
server, it's not always easy or even possible to know the exact state of the
server.

Open sound control
------------------

How does the client communicate with the server? For historical reasons, the
server listens for messages using the `Open Sound Control`_ (aka *OSC*) wire
format.

Like WebSockets or stdin/stdout process pipes and *unlike* HTTP's paired
request/response model, OSC communications are *bidirectional*. Messages go out
from the client to the server, and are not explicitly matched by responses from
the server back to the client. Both client and server may send each other
messages at any moment. By convention, ``scsynth`` sends replies to many
requests, but this is an explicit design decision by the SuperCollider
developers and not a feature of OSC. Sending these response messages is not
enforced by OSC or the UDP or TCP protocols those OSC messages are sent over.

OSC allows for sending :py:class:`messages <supriya.osc.messages.OscMessage>`
and (potentially timestamped) :py:class:`bundles
<supriya.osc.messages.OscBundle>` of other messages or bundles. An OSC message
is basically a list of simple data types. By convention they start with a
string (the *address*) and any subsequent values must be integers, floats,
booleans, other strings, etc. You can think of it as a very, very strict subset
of JSON.

Some OSC messages to the server are considered *synchronous*. The command they
encodeare is enacted immediately.

Other OSC messages to the server are considered *asynchronous*. The command
they encode may take a few moments to come to pass, typically because the
server must perform additional memory allocation or processing whose time
complexity is unknown. Most asynchronous messages to ``scsynth`` may contain
a *completion* message: another OSC message or bundle to be handled once the
initial command has completed. You can think of these as a sort of callback:
"do Y once X completes, however long X takes."

Supriya models all messages from the client to the server, and from the server
back to the client, explicitly as classes, and provides methods on its
:py:class:`~supriya.contexts.realtime.Server` class for constructing and
sending these messages (or bundles thereof) transparently.

Nodes, groups, and synths
-------------------------

What sorts of commands do OSC messages encode, anyways? And what is the server
even doing when it processes audio?

The server contains a number of entities. Perhaps the most crucial of these are
:py:class:`nodes <supriya.contexts.entities.Node>`, which are organized into a
*rooted acyclic digraph*, a *tree*. There are two kinds of nodes:
:py:class:`groups <supriya.contexts.entities.Group>` and :py:class:`synths
<supriya.contexts.entities.Synth>` . Group nodes contain other nodes (either
other groups, or synths) while synths perform audio processing.

When processing audio, the server walks the node tree *depth-first*, starting
from the *root node*, visiting each node in turn. The synth nodes process audio
one after another until every node has been visited. Audio processing in this
framework is relatively deterministic.

The alternative server ``supernova`` introduces parallelism for special groups
called *parallel groups*, and therefore introduces indeterminism. Parallel
groups process their immediate children in *parallel* which means care must be
taken to handle how audio data is read and written by parallelized synths.

Buses and buffers
-----------------

But where do synths read audio data from and write audio data to?

Synths typically read from and write to :py:class:`buses
<supriya.contexts.entities.Bus>`: placeholders for signals. Buses come in two
flavors: *audio-rate* and *control-rate*. Control-rate buses are conceptually
equivalent to *control voltage* in modular synthesizer systems, and audio-rate
buses as conceptually similar to channels on a gigantic mixer. Audio-rate buses
allow us to manage processing signals *sample-by-sample*, while control-rate
buses only allow us to process signals *once per sample-block*. For many
applications, this arrangement is perfectly fine, especially given that the
default sample block size is 64 samples - typically barely more than a
millisecond at most common sample rates.

Synths can also read from and write to *buffers* :py:class:`buffers
<supriya.contexts.entities.Buffer>` : fixed-size arrays of floating point
values. Buffers are used for a variety of purposes: as wavetables, as
envelopes, as samples for samplers, for delay lines, as large-scale parameter
holders, etc. Unlike buses, which change and may (in the case of audio-rate)
zero out every sample block unless touched, buffers maintain their data until
changed.

Also unlike buses - which are instantiated en masse when the server boots and
cannot be increased or decreased in number after booting, buffers must be
explicitly allocated on the server as they require allocating an unknown amount
of additional memory. Buffer allocation is one of the *asynchronous* actions
mentioned above.

Synth definitions and unit generators
-------------------------------------

OK, but *how* do synths process audio?

Just like the node tree is a graph, synths are themselves graphs too. But
instead of being graphs of nodes, they're graphs of :py:class:`unit generators
<supriya.ugens.core.UGen>` (colloquially called *UGens*). Unit generators
perform discrete audio operations: generate a sine tone, process and input
signal through a filter, multiply two inputs together, etc. Some unit
generators can read from audio or control buses, some can write back to those
buses. Some can read from buffers, and others can write back to those buffers.

Unit generators are composed together into graphs called :py:class:`synth
definitions <supriya.ugens.core.SynthDef>` (colloquially called *SynthDefs*).
When a synth is visited during audio processing, each unit generator governed
by that synth is visited in turn, processing its inputs into its outputs.

When instantiating a synth into the node tree, we need to tell it what synth
definition to use. These definitions are conceptually *templates* for synths.
Unlike the node tree's *dynamic* graph, graphs of unit generators are *static*.
Once a synth definition has been defined, it is fixed. Need a different version
with more channels? Make a new synth definition. Like buffer allocation, synth
definition allocation is an *asynchronous* action. Synth definitions can be
arbitrarily large, from as simple as "add a sine tone to an audio bus" to as
complex as "simulate an entire DX-7 hardware synthesizer".

Realtime and non-realtime
-------------------------

Finally, *when* does audio processing take place?

The server actually has two *time* modes: *realtime* (the default) and
*non-realtime*.

When discussing interacting with the server, we typically think in realtime
terms: audio is playing live, right now. Audio inputs are going in live, audio
outputs are going out live. The server is responding to our commands in
realtime. We are literally performing live, *now*. In realtime, a server
receives blocks of samples from your sound card, chops those blocks into
*sample blocks* and then processes each block through the node tree, handing
back the sample block to the soundcard which eventually bundles that sample
block into a hardware output block for performance on your speaker or
headphones.

But the server can also perform *offline* in *non-realtime mode* (colloquially
*NRT* or *NRT mode*). As with realtime, non-realtime performance requires OSC
commands to tell the server what to do. Unlike realtime, those commands must be
timestamped OSC *bundles* because a server in NRT mode has no concept of what
*"now"* means, and those bundles must be passed to the server at startup as a
file called a *score*.

Like ``sclang``, Supriya has a class called
:py:class:`~supriya.contexts.nonrealtime.Score` for modeling constructing this
sequence of OSC bundles. Unlike ``sclang``, Supriya attempts to make the
:py:class:`~supriya.contexts.nonrealtime.Score` interface as close as possible
to the :py:class:`~supriya.contexts.realtime.Server` interface to facilitate
writing logic which is unaware of the current time mode.

NRT servers will process audio *as fast as possible* or *as slow as necessary*
to perform all the computations necessary to generate the desired output. This
makes them ideal for doing audio analysis (e.g. find the maximum amplitude in a
soundfile) or for generating compositions too computationally complex to run in
realtime without causing *buffer under-runs* (i.e. the server cannot process
audio quickly enough to deliver to the soundcard for playback).
