Keyboard input, elaborated
==========================

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/keyboard_input_elaborated>` on GitHub.

..  important::

    This example requires additional third-party packages. Install them with:

    ..  include:: /includes/install-examples.txt

Let's rewrite our keyboard example one more time, and make it into something
more polished.

We'll introduce limits on polyphony, craft a lusher-sounding instrumental
voice, add some effects and compression, and restructure our logic so it
starts to approach what a real musical application might look like.

Re-used components
------------------

As with the previous :doc:`async <keyboard_input_async>` example, we get to
re-use:

- The :py:class:`~examples.keyboard_input.NoteOn` and
  :py:class:`~examples.keyboard_input.NoteOff` event classes.
  
- Both the :py:class:`~examples.keyboard_input.MidiHandler` and
  :py:class:`~examples.keyboard_input.QwertyHandler` input handler classes.

Everything else will change subtly or dramatically in this refactoring.

Synth design
------------

We haven't touched on synthesizer design much in the previous examples, but
we'll introduce some now. Feel free to skip over those sections if they're too
complex.

Polyphony management
--------------------

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: PolyphonyManager

Instruments
-----------

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: Instrument

Instrument voice
````````````````

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: build_instrument_synthdef

..  book::
    :hide:

    >>> from examples.keyboard_input_elaborated import instrument_synthdef
    >>> supriya.graph(instrument_synthdef)

Applications
------------

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: Application

Compression
```````````

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: build_compressor_synthdef

..  book::
    :hide:

    >>> from examples.keyboard_input_elaborated import compressor_synthdef
    >>> supriya.graph(compressor_synthdef)

Granular-halo reverb
````````````````````
..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: build_reverb_synthdef

..  book::
    :hide:

    >>> from examples.keyboard_input_elaborated import reverb_synthdef
    >>> supriya.graph(reverb_synthdef)

Scripting
---------

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: run

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: parse_args

..  literalinclude:: ../../../examples/keyboard_input_elaborated/__init__.py
    :pyobject: main

Invocation
----------

You can invoke the script with ...

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input_elaborated --help

... and you'll see the options necessary to properly run it.

Adding a sub-command will show you additional options:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input_elaborated use-midi --help
