import bisect
from typing import TYPE_CHECKING, Iterator, List, Optional, Tuple

from ..enums import CalculationRate
from ..typing import CalculationRateLike
from .bases import SessionObject

if TYPE_CHECKING:
    from .sessions import Session


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

    def __init__(
        self,
        session: "Session",
        *,
        calculation_rate: CalculationRateLike,
        session_id: int,
        bus_group: Optional["BusGroup"] = None,
    ) -> None:
        SessionObject.__init__(self, session)
        self._bus_group = bus_group
        self._calculation_rate = CalculationRate.from_expr(calculation_rate)
        self._events: List[Tuple[float, float]] = []
        self._session_id = session_id

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        return "<{}>".format(super(Bus, self).__repr__())

    def __float__(self):
        return float(self._session_id)

    def __int__(self):
        return int(self._session_id)

    def __str__(self) -> str:
        map_symbol = "c"
        if self.calculation_rate == CalculationRate.AUDIO:
            map_symbol = "a"
        if self.session_id is None:
            return f"{map_symbol}?"
        elif isinstance(self.session_id, tuple):
            return f"{map_symbol}{self.session_id[0]}:{self.session_id[1]}"
        return f"{map_symbol}{self.session_id}"

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
        assert self.calculation_rate == CalculationRate.CONTROL
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
    def get(self, offset=None) -> float:
        value = self._get_at_offset(offset)
        return value

    def get_map_symbol(self, bus_id: int) -> str:
        if self.calculation_rate == CalculationRate.AUDIO:
            return f"a{bus_id}"
        return f"c{bus_id}"

    @SessionObject.require_offset
    def set_(self, value, offset=None) -> None:
        self._set_at_offset(offset, value)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self) -> Optional["BusGroup"]:
        return self._bus_group

    @property
    def calculation_rate(self) -> CalculationRate:
        return self._calculation_rate

    @property
    def session_id(self):
        return self._session_id

    @property
    def start_offset(self) -> float:
        return float("-inf")

    @property
    def stop_offset(self) -> float:
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

    def __init__(
        self,
        session: "Session",
        *,
        calculation_rate: CalculationRateLike,
        session_id: int,
        bus_count: int = 1,
    ) -> None:
        SessionObject.__init__(self, session)
        self._buses = tuple(
            Bus(
                session,
                bus_group=self,
                calculation_rate=CalculationRate.from_expr(calculation_rate),
                session_id=session_id + i,
            )
            for i in range(bus_count)
        )
        self._calculation_rate = CalculationRate.from_expr(calculation_rate)
        self._session_id = session_id

    ### SPECIAL METHODS ###

    def __contains__(self, item) -> bool:
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

    def __iter__(self) -> Iterator["Bus"]:
        return iter(self.buses)

    def __len__(self) -> int:
        return len(self._buses)

    def __repr__(self) -> str:
        return "<{}>".format(super(BusGroup, self).__repr__())

    def __str__(self) -> str:
        map_symbol = "c"
        if self.calculation_rate == CalculationRate.AUDIO:
            map_symbol = "a"
        session_id = self._session_id
        if session_id is None:
            session_id = "?"
        return "{map_symbol}{session_id}".format(
            map_symbol=map_symbol, session_id=session_id
        )

    ### PUBLIC METHODS ###

    def fill(self, value):
        offset = self.session._active_moments[-1].offset
        for bus in self:
            bus._set_at_offset(offset, value)

    def get(self):
        offset = self.session._active_moments[-1].offset
        return [bus._get_at_offset(offset) for bus in self]

    def get_map_symbol(self, bus_id: int) -> str:
        if self.calculation_rate == CalculationRate.AUDIO:
            return f"a{bus_id}"
        return f"c{bus_id}"

    def index(self, item) -> int:
        return self.buses.index(item)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_count(self) -> int:
        return len(self._buses)

    @property
    def buses(self) -> Tuple["Bus", ...]:
        return self._buses

    @property
    def calculation_rate(self) -> CalculationRate:
        return self._calculation_rate

    @property
    def session_id(self):
        return self._session_id


class AudioInputBusGroup(BusGroup):
    """
    A non-realtime audio input bus group.
    """

    ### INITIALIZER ###

    def __init__(self, session: "Session", *, session_id: int) -> None:
        BusGroup.__init__(
            self,
            session,
            bus_count=session.options.input_bus_channel_count,
            calculation_rate=CalculationRate.AUDIO,
            session_id=session_id,
        )


class AudioOutputBusGroup(BusGroup):
    """
    A non-realtime audio output bus group.
    """

    ### INITIALIZER ###

    def __init__(self, session: "Session", *, session_id: int) -> None:
        BusGroup.__init__(
            self,
            session,
            bus_count=session.options.output_bus_channel_count,
            calculation_rate=CalculationRate.AUDIO,
            session_id=session_id,
        )
