:status: under-construction

Buses
=====

..  self-criticism::

    These docs are still under construction.

:term:`Buses <bus>` are how signals travel through :term:`scsynth`. If
:doc:`nodes <nodes>` make and shape sound, buses are the patch cables running
between them: one synth writes its output to a bus, and another - possibly
much later in the :term:`node tree` - reads from it. Buses also carry
microphone signals in and speaker signals out.

Like :doc:`buffers <buffers>`, :term:`scsynth` boots with a fixed number of
buses. *Audio* buses carry a whole block of samples every control block, while
*control* buses carry just a single value. That distinction is a bus's
:term:`calculation rate`, and we'll look at calculation rates in more detail
later, in the :doc:`synthdefs <synthdefs>` tutorial.

Supriya's :py:class:`~supriya.contexts.entities.Bus` class provides a
:term:`proxy` to one of those buses inside a running :term:`scsynth` process,
and the :py:class:`~supriya.contexts.entities.BusGroup` class models a
contiguous block of them.

Lifecycle
---------

Buses can only be added to running servers, so let’s create a server and boot it:

    >>> server = supriya.Server().boot()

..  note::

    :py:class:`Scores <supriya.contexts.nonrealtime.Score>` are neither online
    nor offline, so you can add buses to them whenever you like.

Creation
````````

Remember that :term:`scsynth` creates all of its buses at boot. Nothing we do
here will make a new one.

When we talk about *allocating* a bus, we're really talking about *leasing*
its ID from the server's bus ID space. The bus already exists; we're just
laying claim to its ID so nobody else is handed the same one.

Allocating a bus group works the same way, except Supriya leases a contiguous
block of IDs in a single operation. Freeing a bus or bus group releases its
IDs back to the pool.

Allocate a bus with::

    >>> control_bus = server.add_bus()

Buses are control rate by default. Allocate an audio bus with the
``calculation_rate`` keyword::

    >>> audio_bus = server.add_bus(calculation_rate="audio")

Allocate a bus group of 8 buses with::

    >>> bus_group = server.add_bus_group(count=8)

Deletion
````````

Unlike nodes, freeing a bus doesn't destroy it. The bus still exists inside
:term:`scsynth`; we're simply giving up our lease on its ID so it can be
handed out again.

Free the two buses with::

    >>> control_bus.free()
    >>> audio_bus.free()

Free the bus group with::

    >>> bus_group.free()

Inspection
----------

Buses and bus groups know a few things about themselves, and can ask the
server about the values they carry.

We freed our buses at the end of the last section, so let's allocate a fresh
control bus, a fresh audio bus, and a bus group of four control buses::

    >>> control_bus = server.add_bus()
    >>> audio_bus = server.add_bus(calculation_rate="audio")
    >>> bus_group = server.add_bus_group(count=4)

Identity and rate
`````````````````

Like :doc:`nodes <nodes>`, every bus has an ``id_`` and a reference to its
context. Control and audio buses have separate ID spaces, so don't be
surprised if two buses share an ``id_`` but differ in calculation rate::

    >>> control_bus.id_, control_bus.context
    >>> audio_bus.id_, audio_bus.context

A bus also knows its :term:`calculation rate`::

    >>> control_bus.calculation_rate
    >>> audio_bus.calculation_rate

A bus group has an ``id_`` too: the ID of the first bus in the block. It
shares its calculation rate with all of its buses::

    >>> bus_group.id_, bus_group.calculation_rate

Bus group contents
``````````````````

Bus groups know how many buses they contain, and can hand them back to you as
:py:class:`~supriya.contexts.entities.Bus` instances::

    >>> len(bus_group)
    >>> bus_group.buses

Bus groups can be indexed, sliced and iterated over, just like a sequence::

    >>> bus_group[0]
    >>> bus_group[1:3]
    >>> for bus in bus_group:
    ...     bus.id_
    ...

Note that the ``id_`` of each bus is one greater than the last. That's what we
mean by a *contiguous* block.

Reading values
``````````````

Control buses carry a single value, which you can ask the server for with
:py:meth:`~supriya.contexts.entities.Bus.get`::

    >>> control_bus.get()

Ask a bus group for its values and you'll get one value for each of its
buses::

    >>> bus_group.get()

If you want a few values starting from a particular bus, use
:py:meth:`~supriya.contexts.entities.Bus.get_range` with a count::

    >>> bus_group[1].get_range(2)

If you've installed Supriya with the ``shm`` extra
(``pip install "supriya[shm]"``), you can pass ``use_shared_memory=True`` to
any of these reads. Instead of sending an OSC message and waiting for a reply,
Supriya will read the values straight out of :term:`scsynth`'s shared memory,
which shaves off a little latency::

    >>> control_bus.get(use_shared_memory=True)
    >>> bus_group.get(use_shared_memory=True)

..  caution::

    Shared memory only works with *local* servers, because the client and
    :term:`scsynth` need to be able to see the same block of memory.

..  caution::

    Only control buses can be read this way. :term:`scsynth` doesn't give us a
    way to read audio buses, because their contents change every control
    block. Asking an audio bus for its value will raise an exception.

..  note::

    Reading a value means asking :term:`scsynth` and waiting for her answer,
    so these methods are only available on realtime contexts. They'll raise a
    :py:class:`~supriya.exceptions.ContextError` on a
    :py:class:`~supriya.contexts.nonrealtime.Score`.

Interaction
-----------

Now that we know how to read control buses, let's write to them.

Setting values
``````````````

Set a control bus' value with :py:meth:`~supriya.contexts.entities.Bus.set`,
then read it back to check our work::

    >>> control_bus.set(0.5)
    >>> control_bus.get()

Set a run of contiguous buses at once with
:py:meth:`~supriya.contexts.entities.Bus.set_range`, which writes one value to
each bus, starting with the bus you call it on::

    >>> bus_group[0].set_range([0.1, 0.2, 0.3, 0.4])
    >>> bus_group.get()

..  caution::

    A single bus knows nothing about the bus group it belongs to, so
    ``set_range()`` does no bounds checking. If you pass more values than
    there are buses left in the group, you'll write right past the end of it,
    into buses that may belong to someone else.

Filling buses
`````````````

To write the *same* value to a range of buses, use
:py:meth:`~supriya.contexts.entities.Bus.fill` with a count and a value::

    >>> bus_group[1].fill(3, 0.9)
    >>> bus_group.get()

Note that the first bus, which we didn't include in the fill, kept its value.

Setting bus groups
``````````````````

:py:meth:`BusGroup.set() <supriya.contexts.entities.BusGroup.set>` covers both
cases. Pass it a sequence and it sets each bus in turn, or pass it a single
number and it fills the whole group::

    >>> bus_group.set([1.0, 2.0, 3.0, 4.0])
    >>> bus_group.get()

    >>> bus_group.set(0.0)
    >>> bus_group.get()

Unlike the single-bus methods, ``BusGroup.set()`` checks its bounds, so it
only ever modifies the buses the group governs.

..  note::

    Unlike reading, writing doesn't require a reply from :term:`scsynth`, so
    you can set and fill buses on a
    :py:class:`~supriya.contexts.nonrealtime.Score` too. Like reads, writes
    accept ``use_shared_memory=True`` for local servers with the ``shm`` extra
    installed.

Integration
-----------

Supriya's :py:class:`~supriya.contexts.entities.Bus` and
:py:class:`~supriya.contexts.entities.BusGroup` classes provide affordances for
interacting with other parts of the system.

Referencing
```````````

Buses and bus groups fulfil ``SupportsInt``, so you can pass them anywhere an
integer ID is expected.

- ``int(bus)`` and ``int(bus_group)`` give back the ``id_`` (for bus groups,
  the ID of the first bus).
- ``float(bus)`` works too.
- Handy when building raw OSC messages or when interpolating IDs into
  :term:`SynthDef` controls.

Mapping controls
````````````````

A synth's control can read from a control or audio bus instead of holding its own
value. That's called *mapping*.

- ``.map_symbol()`` returns the bus' map symbol: ``c<id>`` for control buses
  and ``a<id>`` for audio buses. Bus groups have one too.
- ``Node.map()`` maps node controls to buses by keyword, and unmaps them when
  passed ``None``.
- Audio buses can be mapped too, via ``/n_mapa``.
- TODO: ``Node.map_range()``

Inputs and outputs
``````````````````

Synths read from and write to buses with a family of :term:`UGens <UGen>`.

- :py:class:`~supriya.ugens.In` reads from a bus.
- :py:class:`~supriya.ugens.Out` writes to a bus, mixing with whatever else is
  writing to it that control block.
- :py:class:`~supriya.ugens.ReplaceOut` overwrites the bus instead of mixing.
- :py:class:`~supriya.ugens.XOut` crossfades between the bus' contents and the
  synth's signal.
- :py:class:`~supriya.ugens.InFeedback` reads audio from a bus that hasn't
  been written yet this block, at the cost of a block of delay. Needed when a
  synth earlier in the :term:`node tree` has to read from a synth that comes
  later.
- :py:class:`~supriya.ugens.OffsetOut` writes with sub-block timing, for
  sample-accurate scheduling.

Configuration
-------------

The number of buses available in a context is controlled by its
:py:class:`options <supriya.scsynth.Options>`.

- Set the maximum number of control buses with the
  ``control_bus_channel_count`` keyword.

- Set the maximum number of audio buses with the ``control_bus_channel_count``
  keyword.

- Set the number of *input* audio buses to the server with the
  ``input_bus_channel_count`` keyword.

- Set the number of *output* audio buses to the server with the
  ``output_bus_channel_count`` keyword.

..  note::

    The ``input_bus_channel_count`` and ``output_bus_channel_count`` values are
    independent of what your current soundcard supports. They can be greater
    than or less than the number of available channels, but won't actually
    carry more information if you select a higher value internal to the
    context. Typically you select the same or fewer channels.

These can be set on an :py:class:`~supriya.scsynth.Options` instance passed the
context when initialized or booting, or just as keyword arguments.
