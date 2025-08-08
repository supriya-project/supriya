Keyboard input
==============

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/keyboard_input>` on GitHub.

..  important::

    This example requires additional third-party packages. Install them with:

    ..  include:: /includes/install-examples.txt

Let's introduce some interactivity.

We can play notes with Supriya using a MIDI keyboard. Don't have a MIDI
keyboard available? We'll also support using your computer's QWERTY keyboard
just like you can in Ableton live.

Note events
-----------

What's a "note", anyways?

MIDI represents notes not as durated objects positioned on a timeline, but
instead as pairs of "on" and "off" events. The note starts when an instrument
handles a note "on" event, and it stops when that instrument handles the
corresponding note "off" event. We won't recreate MIDI here exactly, but we
need some simple classes to represent the idea of starting a note with a given
pitch (or *note number*) and loudness (or *velocity*) and stopping a note at a
given pitch. We can do this with a pair of :py:mod:`dataclasses`:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: NoteOn

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: NoteOff

The integer values for ``note_number`` and ``velocity`` will range from ``0``
to ``127``, just like with MIDI. It's an obvious choice for this examples
because we'll literally be using MIDI as an input later on. Massaging all input
values into a consistent ``0-127`` range will remove the need for
special-casing.

..  note::

    We'll use :py:mod:`dataclasses` pervasively in the examples because 1) they
    save vertical space by removing boilerplate, and 2) their requirement to
    use type hints (in `my`_ opinion) aids legibility. Importantly, we don't
    need to write initializers for them.

Managing polyphony
------------------

While "note" events represent *only* the start of stop of a note, we need to
translate these events into the creation and destruction of synths on the
SuperCollider server, and that requires tracking *state*. We'll do this with a
polyphony manager. Our implementation looks like this:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: PolyphonyManager

The polyphony manager's main work is in its
:py:meth:`~examples.keyboard_input.PolyphonyManager.perform` method,
translating note on and note off events into actions to create or destroy
synths on the SuperCollider server. When creating synths, we need to translate
the MIDI ``0-127`` range into Hertz frequency and linear amplitude. We'll use
some conversion helpers to do this. The manager stores state about the notes
and synths in a dictionary, mapping note numbers to synth instances so the
synths can be freed later, when it handles note "off" events. 

The manager also implements a
:py:meth:`~examples.keyboard_input.PolyphonyManager.free_all` method to free
all the synths at once. We'll see both
:py:meth:`~examples.keyboard_input.PolyphonyManager.perform` and
:py:meth:`~examples.keyboard_input.PolyphonyManager.free_all` in use later on.

Handling input
--------------

Now let's build some input handlers.

We have some basic requirements for any input handler:

- It needs to translate raw input into
  :py:class:`~examples.keyboard_input.NoteOn` and
  :py:class:`~examples.keyboard_input.NoteOff` events.

- It needs to start up and listen continuously in the background in a
  non-blocking way.

- It needs to be *decoupled* from the rest of the system. It shouldn't know
  about our :py:class:`~examples.keyboard_input.PolyphonyManager`, only that it
  can pass the generated :py:class:`~examples.keyboard_input.NoteOn` and
  :py:class:`~examples.keyboard_input.NoteOff` events along to some other
  callable, configured when the input handler is instantiated.

We'll define a simple base class for our MIDI and QWERTY input handlers, mainly
to ease type hints. Anytime you encounter a setup / do something / teardown
pattern, a context manager is an obvious choice, so we'll use Python's
:py:func:`contextlib.contextmanager` to decorate our
:py:meth:`~examples.keyboard_input.InputHandler.listen` stub method:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: InputHandler

She doesn't actually do anything, so let's define some concrete
implementations.

Handling MIDI
`````````````

MIDI input is *relatively* simple to setup, at least compared to QWERTY. We'll
use the `python-rtmidi`_ library to listen to MIDI messages from attached
hardware. Let's take a look:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: MidiHandler

The :py:meth:`~examples.keyboard_input.MidiHandler.listen` context manager
creates an :py:class:`rtmidi.MidiIn` instance, points its callback at the
:py:class:`~examples.keyboard_input.MidiHandler`'s
:py:meth:`~examples.keyboard_input.MidiHandler.handle` method, opens a port and
then yields. When it's done yielding it just closes the port. Look closer at
how we treat the callback passed into
:py:meth:`~examples.keyboard_input.MidiHandler.listen` . Rather than store a
reference to the callback function on the handler instance, we use
:py:func:`functools.partial` to "freeze" part of the call to the handler's
:py:meth:`~examples.keyboard_input.MidiHandler.handle` method. This way, our
custom ``callback`` will always be the first argument to
:py:meth:`~examples.keyboard_input.MidiHandler.listen` as long as we're inside
its context block.

MIDI note on and note off messages arrive into our
:py:meth:`~examples.keyboard_input.MidiHandler.handle` method from
:py:mod:`rtmidi` as integer triples. The first integer (the *status*) tells us
what kind of MIDI message it is. For note on and note off messages the second
integer represents the note number, from ``0`` to ``127`` (more than enough to
represent a grand piano's keyboard, which should be good enough for anyone,
right?) and the last integer represents the *velocity* (how fast the key was
pressed, which by convention maps to volume level).

Our :py:meth:`~examples.keyboard_input.MidiHandler.handle` method checks the
first integer to determine if it's handling a note on or note off, ignoring
other types of messages, and then wraps the data into our
:py:class:`~examples.keyboard_input.NoteOn` and
:py:class:`~examples.keyboard_input.NoteOff` dataclasses, calling the
``callback`` callable against them.

Handling QWERTY
```````````````

Input from a computer keyboard is more complicated because we need to simulate
a larger pitch space than we have keys on our computer keyboard. We'll use the
`pynput`_ library to listen for key presses and releases, and mimic `Ableton
Live`_'s QWERTY keyboard feature. Take a look and then let's discuss.

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: QwertyHandler

Like the :py:class:`~examples.keyboard_input.MidiHandler`, the
:py:meth:`~examples.keyboard_input.QwertyHandler.listen` context manager is pretty simple. We create a
:py:class:`pynput.keyboard.Listener`, point it as *two* different callback
methods (one for pressing keys, and another for releasing them ), start it,
yield to the with block, then stop it when we're done. Easy.

Handling those key presses and releases is tricky though. We'll treat
``asdfghjkl;'`` as our white keys with ``a`` mapping to a ``C5`` on a piano
keyboard and ``;`` mapping to an ``F6``, and ``we tyu op`` as black keys
starting from ``C#5``. That's about an octave and a half of notes when we'd
like to simulate the ten-plus octaves available on MIDI. To do this, we'll
store the current octave on the handler, and use the ``z`` and ``x`` keys to
decrement or increment the octave, adding it to the note number mapped from the
other keys.

That's great, but what happens if you change the octave when you're in the
middle of changing the note? When releasing the key, we'd send a
:py:class:`~examples.keyboard_input.NoteOff` event corresponding to a different
pitch than the original :py:class:`~examples.keyboard_input.NoteOn` event,
resulting in "stuck" synths. To fix this, we'll add *state* to the
:py:class:`~examples.keyboard_input.MidiHandler`, storing the note numbers
calculated at the moment each QWERTY key was pressed. When we release the
QWERTY key, rather than re-calculate what the note number should be based on
the current octave, we look up the note number calculated at key press and
issue a :py:class:`~examples.keyboard_input.NoteOff` for that instead.

Integration
-----------

Now we need to stitch together our input handlers, the polyphony manager, and a
server so we can actually hear something. We'll write one
:py:func:`~examples.keyboard_input.run` function with a number of simple nested
functions for the various callbacks our application requires:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: run

A few notes about our :py:func:`~examples.keyboard_input.run` function:

- It takes an :py:class:`~examples.keyboard_input.InputHandler` as its only
  argument, which means we can use the
  :py:class:`~examples.keyboard_input.MidiHandler` and
  :py:class:`~examples.keyboard_input.QwertyHandler` classes interchangeably.
  It doesn't know anything about their specific implementations, just that they
  have a :py:meth:`~examples.keyboard_input.InputHandler.listen` context
  manager method that accepts a ``callback`` callable.

- The :py:class:`~examples.keyboard_input.InputHandler`'s context block simply waits on a
  :py:class:`concurrent.futures.Future` to resolve, nothing more. When the
  future resolves, we exit the context block and quit the server.

- We add setup and teardown logic to our server via lifecycle event callbacks.
  Setup involves loading the :py:class:`~supriya.ugens.core.SynthDef` we'll use
  to create synths, and to wait for it to load before proceeding. Teardown
  involves freeing any synths still playing after we stop listening for input
  events, and then waiting for them to completely fade out before moving on.

- Without getting too deep into systems programming, we'll use a
  :py:func:`signal.signal` callback to listen for ``Ctrl-C`` presses on the
  keyboard. When you press ``Ctrl-C`` to end the script, this callback will set
  the value of the exit future our script is waiting on, allowing it to
  progress to its shutdown logic.

Scripting
---------

Let's put final touches on our script so we can run it from the command-line.

We'll use :py:mod:`argparse` to define the flags we can pass to the script,
with a required *mutually exclusive argument group* forcing us to pick at least
one flag:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: parse_args

Then we just parse the arguments, check which flag was set, create the
appropriate :py:class:`~examples.keyboard_input.InputHandler` and then call
:py:func:`~examples.keyboard_input.run` with it:

..  literalinclude:: ../../../examples/keyboard_input/__init__.py
    :pyobject: main

Of course, we might not know what port to use when playing with MIDI, so we'll
use the ``--list-midi-inputs`` flag to print out available MIDI port numbers
you can pass to the script when running it with ``--use-midi``.

Invocation
----------

You can invoke the script with ...

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input --help

... and you'll see the options necessary to properly run it.

