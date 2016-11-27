# -*- enoding: utf-8 -*-
import bisect
from supriya.tools import synthdeftools
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Bus(SessionObject):
    """
    A non-realtime bus.

    ::

        >>> session = nonrealtimetools.Session()
        >>> bus = session.add_bus('control')
        >>> print(bus)
        <Bus(
            calculation_rate=CalculationRate.CONTROL
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
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        bus_group=None,
        calculation_rate=None,
        ):
        from supriya.tools import nonrealtimetools
        SessionObject.__init__(self, session)
        if bus_group is not None:
            assert isinstance(bus_group, nonrealtimetools.BusGroup)
        self._bus_group = bus_group
        assert calculation_rate is not None
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate
        self._events = []

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

    def _get_format_specification(self):
        from abjad.tools import systemtools
        from supriya.tools import nonrealtimetools
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_positional_names
        values = (agent._get(_) for _ in names)
        values = [
            _ for _ in values
            if not isinstance(_, nonrealtimetools.Session)
            ]
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            repr_is_bracketed=True,
            storage_format_is_bracketed=True,
            storage_format_args_values=values,
            )

    def _set_at_offset(self, offset, value):
        assert self.calculation_rate == synthdeftools.CalculationRate.CONTROL
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
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
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
    def start_offset(self):
        return float('-inf')

    @property
    def stop_offset(self):
        return float('inf')
