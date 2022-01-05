Clocks
======

Supriya provides a collection of musical-time-aware clocks which permit
scheduling callbacks relative to both seconds, beats and measures, and which - by
extension - understand tempo, time signatures and downbeats.

These clocks come in both *threaded* and *asynchronous* flavors, as well as
*online* and *offline*.

*Threaded* clocks handle callbacks in their own thread, while *asynchronous*
clocks hook into an :py:mod:`asyncio` event loop. Use threaded clocks when
experimenting interactively in the terminal or building simple applications.
Use asynchronous clocks when building more complex applications which integrate
with other :py:mod:`asyncio`-aware libraries like `aiohttp`_,
`python-prompt-toolkit`_ or `pymonome`_.

*Offline* clocks implement the same interface as their *online* counterparts,
but process their callbacks as fast as possible, regardless of the amount of
real time consumed. This makes them suitable for unit-testing logic expecting
online clocks, or for implementing non-realtime rendering of usually-online
musical patterns.

Lifecycle
---------

Creating
````````

Instantiate a *threaded* clock with::

    >>> clock = supriya.Clock()

Starting and stopping
`````````````````````

Start a *threaded* clock with::

    >>> clock.start()

Stop a *threaded* clock with::

    >>> clock.stop()

Scheduling
----------

Let's consider a simple callback function::

    >>> def callback(context):
    ...     print(f"The current offset is: {context.current_moment.offset}")
    ...

All clock callbacks need to accept *at least* a ``context`` argument, to which
the clock will pass a :py:class:`~supriya.clocks.ephemera.ClockContext` object.

Scheduling
``````````

We can schedule that procedure with::

    >>> clock.schedule(callback)

Scheduling callbacks returns an event ID.

Canceling
`````````

We can use the event ID to cancel the callback if it hasn't already occurred::

    >>> clock.cancel(0)

Cueing
``````

We can also *cue* callbacks, scheduling them to occur at some quantized offset
in the future, e.g. on the next beat or downbeat::

    >>> clock.cue(callback)

Callbacks
---------

Let's consider a more complicated callback function::

    >>> def callback(
    ...     context,
    ...     salutation,
    ...     delta=0.25,
    ...     max_repeats=0,
    ...     time_unit=supriya.clocks.TimeUnit.SECONDS,
    ... ):
    ...     print(f"{salutation}: {context.current_moment.offset}")
    ...     if max_repeats and context.event.invocations < max_repeats:
    ...         print("Re-scheduling")
    ...         return delta, time_unit
    ...     else:
    ...         print("Bailing!")
    ...

Arguments
`````````

- positional arguments
- keyword arguments

Deltas
``````

- none
- single float
- pair of float and time unit or int

Contexts, moments, events
`````````````````````````

- contexts
- moments, current and expected
- events, invocations

Musical time
------------

Like callbacks, changes to tempo and time signature can be triggered
"immediately", scheduled at an absolute point in the future, or cued at some
quantization relative the current time.

Tempo
`````

Time signatures
```````````````

Async clocks
------------

*Async* clocks have identical APIs to *threaded* clocks with three differences:

- their :py:meth:`~supriya.clocks.asynchronous.AsyncClock.start` method is async,
- their :py:meth:`~supriya.clocks.asynchronous.AsyncClock.stop` method is async, and
- scheduled callbacks may also be async.

Instantiate an *async* clock with::

    >>> clock = supriya.AsyncClock()

Offline clocks
--------------

Debugging
---------

.. _aiohttp: https://docs.aiohttp.org
.. _pymonome: https://github.com/artfwo/pymonome
.. _python-prompt-toolkit: https://python-prompt-toolkit.readthedocs.io
