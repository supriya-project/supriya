# -*- enoding: utf-8 -*-
import bisect
import supriya.synthdefs
from supriya.nonrealtime.SessionObject import SessionObject


class Bus(SessionObject):
    """
    A non-realtime bus.

    ::

        >>> import supriya.nonrealtime
        >>> session = supriya.nonrealtime.Session()
        >>> bus = session.add_bus('control')
        >>> print(repr(bus))
        <Bus(
            calculation_rate=CalculationRate.CONTROL,
            session=<Session>,
            session_id=0,
            )>

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

    __documentation_section__ = 'Session Objects'

    __slots__ = (
        '_bus_group',
        '_calculation_rate',
        '_events',
        '_session',
        '_session_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        bus_group=None,
        calculation_rate=None,
        session_id=None,
        ):
        import supriya.nonrealtime
        SessionObject.__init__(self, session)
        self._session_id = session_id
        if bus_group is not None:
            assert isinstance(bus_group, supriya.nonrealtime.BusGroup)
        self._bus_group = bus_group
        assert calculation_rate is not None
        calculation_rate = supriya.synthdefs.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate
        self._events = []

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{}>'.format(super(Bus, self).__repr__())

    def __str__(self):
        map_symbol = 'c'
        if self.calculation_rate == supriya.synthdefs.CalculationRate.AUDIO:
            map_symbol = 'a'
        session_id = self._session_id
        if session_id is None:
            session_id = '?'
        elif isinstance(session_id, tuple):
            session_id = '{}:{}'.format(session_id[0], session_id[1])
        return '{map_symbol}{session_id}'.format(
            map_symbol=map_symbol,
            session_id=session_id,
            )

    ### PRIVATE METHODS ###

    def _get_at_offset(self, offset):
        events = self._events
        if not events:
            return 0.
        index = bisect.bisect_left(events, (offset, 0.))
        if len(events) <= index:
            old_offset, value = events[-1]
        else:
            old_offset, value = events[index]
        if old_offset == offset:
            return value
        index -= 1
        if index < 0:
            return 0.
        _, value = events[index]
        return value

    def _set_at_offset(self, offset, value):
        assert self.calculation_rate == supriya.synthdefs.CalculationRate.CONTROL
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
        if self.calculation_rate == supriya.synthdefs.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
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
        return float('-inf')

    @property
    def stop_offset(self):
        return float('inf')
