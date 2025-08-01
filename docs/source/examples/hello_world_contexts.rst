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

Performance logic
-----------------

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: play_synths

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: stop_synths

Context management
------------------

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: run_threaded

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: run_async

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: run_nonrealtime

Scripting
---------

Now that we have three different ways of creating contexts to use our
context-agnostic performance logic, we need a way to yoke them into a script.

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: parse_args

..  literalinclude:: ../../../examples/hello_world_contexts/hello_world_contexts.py
    :caption:
    :pyobject: main

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
