Hello, world!
=============

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/hello_world>` on GitHub.

Supriya's `"hello, world!"`_ is a little longer than most traditional "hello,
world!" recipes, because playing a sound from scratch requires more than one step:

- We need a :doc:`server <../tutorials/servers>`, booted and online

- We need to find (or define) a :doc:`SynthDef <../tutorials/synthdefs>` to act
  as the template for the synths that actually make sound

- We need to allocate that SynthDef on the running server, and we need to wait for
  allocation to complete (because SynthDef allocation is an asynchronous command)

- Once the SynthDef finishes allocating, we need to create one or more
  :doc:`synths <../tutorials/nodes>`

- We need to give those synths some time to play so we can actually hear
  them

- And we should be good and clean up after ourselves: release the synths, wait
  for them to fade out, then quit the running server

All of this logic is outlined in the example's ``main`` function:

..  literalinclude:: ../../../examples/hello_world/hello_world.py
    :pyobject: main

Invocation
----------

You can invoke the script with ...

..  shell::
    :cwd: ../examples/hello_world
    :rel: ..
    :user: josephine
    :host: laptop

    python hello_world.py

You should hear a C-major chord play for a few seconds, then fade out quickly
before the script exits.

Hello, world!
