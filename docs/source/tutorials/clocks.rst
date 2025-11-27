:status: under-construction

Clocks
======

..  self-criticism::

    These docs are still under construction.

Supriya provides a collection of musical-time-aware clocks for scheduling
callbacks relative to both seconds, beats and measures, and which - by
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

Time
----

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

Starting at a specific time
```````````````````````````

Scheduling
----------

We can schedule callbacks to run at some absolute point in time in the future,
both wall time in seconds or a musical offset. We can also *cue* callbacks on a
musical grid, relative to the time boundary of some musical event, e.g. "on the
next 1/4 note" or "on the next downbeat".

Callbacks
`````````

Let's taks a look at a simple callback function::

    >>> def callback(context):
    ...     print(f"The current offset is: {context.desired_moment.offset}")
    ...

All clock callbacks need to accept *at least* a ``context`` argument, to which
the clock will pass a :py:class:`~supriya.clocks.core.ClockContext` object.

The ``context`` tells the callback about what time it currently is - at the
point of execution -, what time we *desired* to execute the callback at - in
case there's drift that you need to account for -, and what the event that
triggered the callback is - encoding information about the default args,
kwargs, and number of invocations to date.

We'll dig deeper into the :py:class:`~supriya.clocks.core.ClockContext` and
:py:class:`~supriya.clocks.core.Moment` classes further down.

Scheduling immediately
``````````````````````

We can schedule that procedure to run immediately with::

    >>> clock.schedule(callback)

Note that scheduling callbacks returns an event ID.

If the clock is already running, the callback will be queued and eventually
executed. If the clock isn't running, the callback will wait until it starts.

Scheduling in the future
````````````````````````

We can schedule a callback to run at a specific time in the future, e.g. 1
second from now, with::

    >>> import time
    >>> id_ = clock.schedule(callback, time.time() + 1)

Canceling
`````````

We can use the event ID to cancel the callback, assuming it hasn't already
occurred::

    >>> clock.cancel(id_)

Cueing on a grid
`````````````````

We can also *cue* callbacks, scheduling them to occur at some quantized offset
in the future, e.g. on the next 1/4 beat::

    >>> _ = clock.cue(callback, quantization="1/4")

... or the next downbeat::

    >>> _ = clock.cue(callback, quantization="1M")

Valid quantizations include:

- ``8M``
- ``4M``
- ``2M``
- ``1M``
- ``1/2``
- ``1/2T``
- ``1/4``
- ``1/4T``
- ``1/8``
- ``1/8T``
- ``1/16``
- ``1/16T``
- ``1/32``
- ``1/32T``
- ``1/64``
- ``1/64T``
- ``1/128``

... much like in Ableton Live. ``M`` indicates a measure, regardless of time
signature. ``T`` indicates a triplet.

Let's start the clock and wait for the scheduled callbacks to run::

    >>> clock.start()

Not very exciting! They all executed at the same time. Why? Because both the
*immediately* scheduled callback and the two *quantized* callbacks all aligned
on the initial 0 offset when the clock started.

Let's dig deeper into callbacks so we can get some more interesting output ...

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

Deltas
``````

- none
- single float
- pair of float and time unit or int

Arguments
`````````

- positional arguments
- keyword arguments

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

- their :py:meth:`~supriya.clocks.AsyncClock.start` method is async,
- their :py:meth:`~supriya.clocks.AsyncClock.stop` method is async, and
- scheduled callbacks may also be async.

Instantiate an *async* clock with::

    >>> async_clock = supriya.AsyncClock()

Start the async clock with::

    >>> await async_clock.start()

Stop the async clock with::

    >>> await async_clock.stop()

Offline clocks
--------------

Debugging
---------
