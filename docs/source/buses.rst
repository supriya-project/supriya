Buses
=====

- what is a bus?
- buses vs bus groups
- calculation rates

Lifecycle
---------

Buses can only be added to running servers, so let’s create one and boot it:

    >>> server = supriya.Server().boot()

.. note::

   :py:class:`Scores <supriya.contexts.nonrealtime.Score>` are neither online
   nor offline, so you can add buses to them whenever you like.

Creation
````````

- what is allocation? leasing, block allocation

Allocate a bus with::

    >>> bus = server.add_bus()

Allocate a bus group of 8 buses with::

    >>> bus_group = server.add_bus_group(count=8)

Deletion
````````

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

The number of buses available in a context is controlled by its options.

- Options.control_bus_channel_count
- Options.audio_bus_channel_count
- Options.input_bus_channel_count
- Options.output_bus_channel_count
