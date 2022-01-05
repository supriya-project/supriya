import bisect

import supriya.synthdefs
from supriya.nonrealtime.bases import SessionObject


class Bus(SessionObject):
    """
    A non-realtime bus.

    ::

        >>> import supriya.nonrealtime
        >>> session = supriya.nonrealtime.Session()
        >>> bus = session.add_bus("control")
        >>> print(repr(bus))
        <Bus(<Session>, calculation_rate=CalculationRate.CONTROL, session_id=0)>

    ::

        >>> with session.at(1):
        ...     bus.set_(0.5)
        ...
        >>> with session.at(3):
        ...     bus.set_(0.75)
        ...

    ::

        >>> for offset in range(5):
        ...     with session.at(offset):
        ...         value = bus.get()
        ...         print(offset, value)
        ...
        0 0.0
        1 0.5
        2 0.5
        3 0.75
        4 0.75

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_bus_group",
        "_calculation_rate",
        "_events",
        "_session",
        "_session_id",
    )

    ### INITIALIZER ###

    def __init__(self, session, bus_group=None, calculation_rate=None, session_id=None):
        import supriya.nonrealtime

        SessionObject.__init__(self, session)
        self._session_id = session_id
        if bus_group is not None:
            assert isinstance(bus_group, supriya.nonrealtime.BusGroup)
        self._bus_group = bus_group
        assert calculation_rate is not None
        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        self._calculation_rate = calculation_rate
        self._events = []

    ### SPECIAL METHODS ###

    def __repr__(self):
        return "<{}>".format(super(Bus, self).__repr__())

    def __float__(self):
        return float(self._session_id)

    def __int__(self):
        return int(self._session_id)

    def __str__(self):
        map_symbol = "c"
        if self.calculation_rate == supriya.CalculationRate.AUDIO:
            map_symbol = "a"
        session_id = self._session_id
        if session_id is None:
            session_id = "?"
        elif isinstance(session_id, tuple):
            session_id = "{}:{}".format(session_id[0], session_id[1])
        return "{map_symbol}{session_id}".format(
            map_symbol=map_symbol, session_id=session_id
        )

    ### PRIVATE METHODS ###

    def _get_at_offset(self, offset):
        events = self._events
        if not events:
            return 0.0
        index = bisect.bisect_left(events, (offset, 0.0))
        if len(events) <= index:
            old_offset, value = events[-1]
        else:
            old_offset, value = events[index]
        if old_offset == offset:
            return value
        index -= 1
        if index < 0:
            return 0.0
        _, value = events[index]
        return value

    def _set_at_offset(self, offset, value):
        assert self.calculation_rate == supriya.CalculationRate.CONTROL
        events = self._events
        event = (offset, value)
        if not events:
            events.append(event)
            return
        index = bisect.bisect_left(events, event)
        if len(events) <= index:
            events.append(event)
        old_offset, _ = events[index]
        if old_offset == offset:
            events[index] = event
        else:
            events.insert(index, event)

    ### PUBLIC METHODS ###

    @SessionObject.require_offset
    def get(self, offset=None):
        value = self._get_at_offset(offset)
        return value

    def get_map_symbol(self, bus_id):
        import supriya.synthdefs

        if self.calculation_rate == supriya.CalculationRate.AUDIO:
            map_symbol = "a"
        else:
            map_symbol = "c"
        map_symbol += str(bus_id)
        return map_symbol

    @SessionObject.require_offset
    def set_(self, value, offset=None):
        self._set_at_offset(offset, value)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self):
        return self._bus_group

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def session_id(self):
        return self._session_id

    @property
    def start_offset(self):
        return float("-inf")

    @property
    def stop_offset(self):
        return float("inf")


class BusGroup(SessionObject):
    """
    A non-realtime bus group.

    ::

        >>> import supriya.nonrealtime
        >>> session = supriya.nonrealtime.Session()
        >>> bus_group = session.add_bus_group(3)
        >>> print(repr(bus_group))
        <BusGroup(<Session>, bus_count=3, calculation_rate=CalculationRate.CONTROL, session_id=0)>

    ::

        >>> with session.at(1):
        ...     bus_group[0].set_(0.333)
        ...
        >>> with session.at(3):
        ...     bus_group.fill(0.5)
        ...
        >>> with session.at(5):
        ...     bus_group[1].set_(0.666)
        ...     bus_group[2].set_(0.75)
        ...

    ::

        >>> for offset in range(7):
        ...     with session.at(offset):
        ...         values = bus_group.get()
        ...         print(offset, values)
        ...
        0 [0.0, 0.0, 0.0]
        1 [0.333, 0.0, 0.0]
        2 [0.333, 0.0, 0.0]
        3 [0.5, 0.5, 0.5]
        4 [0.5, 0.5, 0.5]
        5 [0.5, 0.666, 0.75]
        6 [0.5, 0.666, 0.75]

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buses", "_calculation_rate", "_session", "_session_id")

    ### INITIALIZER ###

    def __init__(self, session, bus_count=1, calculation_rate=None, session_id=None):
        import supriya.nonrealtime

        SessionObject.__init__(self, session)
        self._session_id = session_id
        assert calculation_rate is not None
        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        self._calculation_rate = calculation_rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            supriya.nonrealtime.Bus(
                session,
                bus_group=self,
                calculation_rate=self.calculation_rate,
                session_id=(session_id, i),
            )
            for i in range(bus_count)
        )

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return self.buses.__contains__(item)

    def __float__(self):
        return float(self._session_id)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buses[item]
        elif isinstance(item, slice):
            return tuple(self._buses[item])

    def __int__(self):
        return int(self._session_id)

    def __iter__(self):
        return iter(self.buses)

    def __len__(self):
        return len(self._buses)

    def __repr__(self):
        return "<{}>".format(super(BusGroup, self).__repr__())

    def __str__(self):
        map_symbol = "c"
        if self.calculation_rate == supriya.CalculationRate.AUDIO:
            map_symbol = "a"
        session_id = self._session_id
        if session_id is None:
            session_id = "?"
        return "{map_symbol}{session_id}".format(
            map_symbol=map_symbol, session_id=session_id
        )

    ### PUBLIC METHODS ###

    def fill(self, value):
        assert self.session._active_moments
        offset = self.session._active_moments[-1].offset
        for bus in self:
            bus._set_at_offset(offset, value)

    def get(self):
        assert self.session._active_moments
        offset = self.session._active_moments[-1].offset
        values = [bus._get_at_offset(offset) for bus in self]
        return values

    def get_map_symbol(self, bus_id):
        import supriya.synthdefs

        if self.calculation_rate == supriya.CalculationRate.AUDIO:
            map_symbol = "a"
        else:
            map_symbol = "c"
        map_symbol += str(bus_id)
        return map_symbol

    def index(self, item):
        return self.buses.index(item)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_count(self):
        return len(self._buses)

    @property
    def buses(self):
        return self._buses

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def session_id(self):
        return self._session_id


class AudioInputBusGroup(BusGroup):
    """
    A non-realtime audio input bus group.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, session):
        calculation_rate = supriya.CalculationRate.AUDIO
        bus_count = session.options.input_bus_channel_count
        BusGroup.__init__(
            self, session, bus_count=bus_count, calculation_rate=calculation_rate
        )


class AudioOutputBusGroup(BusGroup):
    """
    A non-realtime audio output bus group.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, session):
        calculation_rate = supriya.CalculationRate.AUDIO
        bus_count = session.options.output_bus_channel_count
        BusGroup.__init__(
            self, session, bus_count=bus_count, calculation_rate=calculation_rate
        )
