Hello, world!, debugged
=======================

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/hello_world_debugged>` on GitHub.

Let's revisit aspects of the :doc:`previous <hello_world>` :doc:`two
<hello_world_contexts>` `"hello, world!"`_ examples and introduce a variety of
debugging techniques.

Performance logic
-----------------

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :caption:
    :pyobject: play_synths

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :caption:
    :pyobject: stop_synths

Debugging
---------

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :caption:
    :pyobject: debug

..  literalinclude:: ../../../examples/hello_world_debugged/hello_world_debugged.py
    :caption:
    :pyobject: main

Invocation
----------

You can invoke the script with ...

..  shell::
    :cwd: ../examples/hello_world_debugged
    :rel: ..
    :user: josephine
    :host: laptop

    python hello_world_debugged.py
