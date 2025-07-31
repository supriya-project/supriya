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

- **OSC transcripts**: Did I send the messages I thought I sent?

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
must be realtime, so we can rely on it both supporting a concept of
timestamp-free OSC bundling.

Debugging
---------

A context manager!

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :pyobject: debug

Integration
-----------

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :pyobject: main

Invocation
----------

You can invoke the script and see its (very verbose) output with ...

..  shell::
    :cwd: ../examples/hello_world_debugged
    :rel: ..
    :user: josephine
    :host: laptop

    python hello_world_debugged.py
