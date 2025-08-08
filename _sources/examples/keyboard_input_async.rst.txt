Keyboard input, async
=====================

..  info::

    See the :si-icon:`octicons/mark-github-16` :github-tree:`full example
    source code <examples/keyboard_input_async>` on GitHub.

..  important::

    This example requires additional third-party packages. Install them with:

    ..  include:: /includes/install-examples.txt

Let's revisit the :doc:`previous keyboard input example <keyboard_input>`, but
this time we'll refactor it to make it work with :py:mod:`asyncio`. Compared to
the first keyboard input example, this is actually a walk in the park. Now we
get to see why the previous example enforced strict decoupling between logical
components.

Re-used components
------------------

We get to re-use many of the components from the non-async keyboard input
example:

- The :py:class:`~examples.keyboard_input.NoteOn` and
  :py:class:`~examples.keyboard_input.NoteOff` are just event placeholders, so
  don't need any change for use with :py:mod:`asyncio`.

- The :py:class:`~examples.keyboard_input.PolyphonyManager` acts against a
  generic write-only :py:class:`~supriya.contexts.core.Context` which makes it
  concurrency-agnostic.

- And both the :py:class:`~examples.keyboard_input.MidiHandler` and
  :py:class:`~examples.keyboard_input.QwertyHandler` classes take callbacks for
  their :py:meth:`~examples.keyboard_input.InputHandler.listen` context
  manager, decoupling them from any concurrency-specific logic. While their
  callbacks can't be async functions, they can still synchronously interact
  with code that other async logic relies on, like queues, futures, or even
  async tasks.

- We even get to re-use the argument parsing logic, as nothing changes there.

Integration
-----------

The core difference between the sync and async examples is in the
:py:func:`~examples.keyboard_input_async.run` implementation. The async version
sprinkles the ``async`` keyword into various locations, e.g. around booting,
syncing, quitting, waiting on futures, etc. But it also has some deeper logical
differences. Take a look, and then we'll discuss:

..  literalinclude:: ../../../examples/keyboard_input_async/__init__.py
    :pyobject: run

The key difference is in how the input handling logic - which runs in a
background thread - interacts with the async code running on the event loop in
the main thread. In the previous example the input handlers were directly
connected to the polyphony manager's
:py:meth:`~examples.keyboard_input.PolyphonyManager.perform` method, but here
we mediate the interaction via a :py:class:`~asyncio.Queue`. The input handlers
safely drop events onto the queue using
:py:meth:`~asyncio.loop.call_soon_threadsafe`, and a separate coroutine
(``queue_consumer``) runs forever in the event loop, waiting on events to pull
off the queue and performing thowe against the polyphony manager.

We create the queue consumer as a task just before input handling starts and
hold a reference to it so it doesn't get garbage collected, and we cancel that
task the after the exit future resolves, once we've shut down input handling.

..  note::

    There are a lot of different ways of structuring async code (just like any
    code), and of integrating threaded code with async code. `I`_'ve structured
    this async example to stay as close as possible to the sync version for the
    sake of pedagogy. It's possible to implement this example without the queue
    as intermediary, but I like how it forces us to think explicitly about the
    boundaries between background threads and the event loop. As application
    complexity grows, navigating these thread boundaries becomes crucial, so
    let's get used to it a little earlier.

Scripting
---------

Like the :py:func:`~examples.keyboard_input_async.run` function, the
:py:func:`~examples.keyboard_input_async.main` function looks very similar to
the previous version. We're merely wrapping the calls to
:py:func:`~examples.keyboard_input_async.run` in :py:func:`asyncio.run` to
ensure the resulting coroutines are executed (and completed) in an event loop.

..  literalinclude:: ../../../examples/keyboard_input_async/__init__.py
    :pyobject: main

Invocation
----------

You can invoke the script with ...

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    python -m examples.keyboard_input_async --help

... and you'll see the options necessary to properly run it.
