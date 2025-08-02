Hello, world!, debugged
=======================

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/hello_world_debugged>` on GitHub.

Let's revisit aspects of the :doc:`previous <hello_world>` :doc:`two
<hello_world_contexts>` `"hello, world!"`_ examples and introduce a variety of
debugging techniques.

It's not uncommon to wonder "why isn't the audio I expect happening?" We have a
variety of ways to debug this with Supriya (although your volume could always
just be too low).

We'll employ:

- **Server logging**: Did it boot up? Has it reported any errors?

- **Server status**: Is my sample rate correct? Do the counts of nodes, of
  synths, of synthdefs make sense to me?

- **Node tree queries**: Is the structure of nodes on the server what I expect?

- **OSC transcripts**: Did I send the messages I thought I sent? Did I receive
  the message I should have received?

Performance logic
-----------------

The performance logic is almost exactly the same as in the
:doc:`hello_world_contexts` example:

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :pyobject: play_synths

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :pyobject: stop_synths

One small difference, just to save some vertical space in the ``main()`` function is
to move the use of :py:meth:`~supriya.contexts.core.Context.at` inside the two
performance functions. Because we're querying the context state, the context
*must* be realtime, so we can rely on it supporting timestamp-free OSC bundling.

Debugging
---------

OK, let's debug our performance.

We'll write a context manager, facilitated by Python's
:py:func:`contextlib.contextmanager` decorator, to debug the state of the
server and (optionally!) any operations we performed against it:

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :pyobject: debug

The context manager will let us start capturing OSC messages sent and received
into a transcript, *yield* so we can perform an action against the server if we
wish, and when we're done yielding we'll print out:

- a header string,

- the server's *status*,

- any messages we *sent to* or *received from* the server, excluding the
  ``/status`` and ``/status.reply`` messages that are always coming and going
  during standard operations,

- and the server's *node tree*.

Integration
-----------

Now let's sprinkle that debugging context manager throughout our ``main`` function.

We'll also turn on logging output (set to a base level of ``WARNING`` so we
don't see too much) and then dial in the :py:mod:`supriya.scsynth` logger to
``INFO`` so we can see info about the server during booting and quitting.

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :pyobject: main

..  note::

    While the ``with debug(...):``` lines come *before* the operations we want
    to debug, their output actually comes *after*. Inside our debugging context
    manager, the body of our ``with`` block executes at the moment we
    ``yield``, and everything after the ``yield`` keyword occurs when we exit
    that ``with`` block. This might look a little "backwards" in our ``main()``
    function, but sit with it.

Invocation
----------

You can invoke the script and see its (very verbose) output with ...

..  shell::
    :cwd: ../examples/hello_world_debugged
    :rel: ..
    :user: josephine
    :host: laptop

    python hello_world_debugged.py

That's a lot of output! Depending on your application, you may need to dial it
down, or dial it up. Now you have the building blocks to do so.
