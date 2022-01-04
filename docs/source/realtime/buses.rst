Buses
=====

- what is a bus?
- buses vs bus groups
- calculation rates

Lifecycle
---------

Buses can only be added to running servers, so let’s create one and boot it:

    >>> server = supriya.Server().boot()

Creation
````````

- what is allocation? leasing, block allocation

Allocate a bus with::

    >>> bus = server.add_bus()

Allocate a bus group of 8 buses with::

    >>> bus_group = server.add_bus_group()

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
- .bus_group.children
- .get()

Interaction
-----------

- .set_()

Integration
-----------

Referencing
```````````

- .__int__()

Mapping controls
````````````````

- .map_symbol

Inputs and outputs
``````````````````

- In
- Out
- InFeedback
- OffsetOut
- XOut
- ReplaceOut

Lower level APIs
----------------

Bare allocation
```````````````

- .allocate()
