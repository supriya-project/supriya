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
:term:`calculation rate`.

The :py:class:`~supriya.contexts.entities.Bus` class provides a :term:`proxy`
to one of those buses inside a running :term:`scsynth` process, and the
:py:class:`~supriya.contexts.entities.BusGroup` class models a contiguous
block of them. Let's start patching things together...

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

    >>> bus = server.add_bus()

Allocate a bus group of 8 buses with::

    >>> bus_group = server.add_bus_group(count=8)

Deletion
````````

Unlike nodes, freeing a bus doesn't destroy it. The bus still exists inside
:term:`scsynth`; we're simply giving up our lease on its ID so it can be
handed out again.

Free a bus with::

    >>> bus.free()

Free a bus group with::

    >>> bus_group.free()

Inspection
----------

- .bus_id
- .calculation_rate
- .bus_group.buses
- .get()
- .get_range()

Interaction
-----------

- .set_()
- .fill()

Integration
-----------

Referencing
```````````

- .__int__()

Mapping controls
````````````````

- .map_symbol()
- Node.map()
- TODO: Node.map_range()

Inputs and outputs
``````````````````

- In
- Out
- InFeedback
- OffsetOut
- XOut
- ReplaceOut

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
