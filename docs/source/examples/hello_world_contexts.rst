Hello, world!, context-agnostic
===============================

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/hello_world_contexts>` on GitHub.

Let's revisit the first `"hello, world!"`_ :doc:`example <hello_world>` and
apply the concept of :doc:`contexts <../tutorials/contexts>` to create the same
C-major chord in non-realtime, "sync" realtime and "async" realtime contexts.

We'll demonstrate how some code can be "context-agnostic": it doesn't care if
you're running it live or using it to create a pre-recorded audio file offline.

This might seem a little abstract, but it's helpful for code re-use, and is
foundational for more complex audio applications. Remember how commercial DAWs
let you both *play* your song live and also *render* it to disk as quickly as
possible? Context-agnostic performance logic is part of unlocking that.

Performance logic
-----------------

Let's extract some performance logic out of the first :doc:`"hello, world!"
example <hello_world>`.

We can pull out the logic for starting the chord into its own function, passing
the context in as an argument, and returning the list of synths when we're
done:

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: play_synths

..  note::

    Look closely at the context usage when starting the chord: we don't see any
    usage of :py:meth:`~supriya.contexts.core.Context.at` to specify when the
    chord plays. Realtime and non-realtime contexts have subtly different
    semantics around timestamps both in terms of whether timestamps are
    mandatory and what the exact time in the timestamp should be. Because of
    those different semantics, we'll treat setting up the
    :py:class:`~supriya.contexts.core.Moment` as a context-specific
    implementation detail external to this function.

And we can pull out the logic for stopping the chord into its own function,
passing a list of synths in as an argument, and return nothing because there's
nothing else to be done:

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: stop_synths

Nice. We've decoupled playing the chord from stopping the chord, and we've
removed any notion of a concrete context type. These functions can work with
both servers and scores interchangeably.

Context management
------------------

While having context-agnostic logic is great, we still need specific
contexts to run our context-agnostic code with.

Let's create separate functions for playing our C-major chord: two realtime
functions using a :py:class:`~supriya.contexts.realtime.Server` and
:py:class:`~supriya.contexts.realtime.AsyncServer` respectively, and one
non-realtime function using a :py:class:`~supriya.contexts.nonrealtime.Score`.

Threaded realtime
`````````````````

Performing with a threaded server is simple, and looks very much like an
abridged version of the ``main`` function from the very first example:

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: run_threaded

Async realtime
``````````````

Performing with an async server is virtually identical to performing with a
threaded server. The only differences are the server's class name, and a
sprinkling of ``async`` and ``await`` keywords (and yes, ``await
asyncio.sleep()`` instead of ``time.sleep()``):

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: run_async

Booting, quitting and sleeping are all ``async`` operations in this paradigm,
but sending messages to the context doesn't change at all. "Writes" or
"mutations" against the server are never an asynchronous operation. We just
fire them off.

Non-realtime
````````````

Performing with a non-realtime score is a little different. While the score
doesn't need to be booted or quit, we *do* have to be absolutely explicit about
when everything happens. Non-realtime contexts have no concept of "now", so
every moment needs to have an explicit timestamp.

We open a moment at ``0`` seconds and start playing the synths. We don't need
to sleep since nothing is happening live, so instead we open a second moment at
``4`` seconds to stop playing the synths. And to handle the same ``1`` second
fade out that the realtime functions achieve via a final ``sleep(1)``, we just
open a third moment at ``5`` seconds and... *do nothing*. The final no-op
operation against the context just signals to non-realtime rendering that we
should keep processing audio until that timestamp.

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: run_nonrealtime

..  note::

    The timestamps used with scores are all absolute, starting from ``0``
    seconds.

    You don't need to open moments in any particular order: the moment at ``5``
    seconds could've been used before the moments at ``4`` or ``0``. But
    stopping the synths had to be applied after staring them, because we still
    needed :py:class:`~supriya.contexts.entities.Synth` objects with IDs to act
    against.

    Timestamps can be visited multiple times too, allowing you to make multiple
    passes against the same score. Additional commands run at the same
    timestamp will be appended to the sequence of commands to be run at that
    timestamp.

The call at the end to :py:func:`~supriya.io.play` renders the score to disk
and opens the result in your default audio player.

Scripting
---------

Now that we have three different ways of creating contexts to use our
context-agnostic performance logic, we need a way to yoke them into a script.

Our ``main`` function parses some command-line arguments, and then calls the
appropriate ``run_...()`` function depending on what we passed to the CLI on
invocation:

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: main

And, for simplicity, we'll wrap up the CLI argument parsing into its own
function, using Python's :py:mod:`argparse` module to create an argument
parser, create a mandatory mutually-exclusive group of flags, and then parse
whatever CLI arguments were passed when we run the script:

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :pyobject: parse_args

Invocation
----------

You can invoke the script with ...

..  shell::
    :cwd: ../examples/hello_world_contexts
    :rel: ..
    :user: josephine
    :host: laptop

    python hello_world_contexts.py --help

... and you'll see the options necessary to properly run it.

For example:

..  shell::
    :cwd: ../examples/hello_world_contexts
    :rel: ..
    :user: josephine
    :host: laptop

    python hello_world_contexts.py --realtime-threaded
