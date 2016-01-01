# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools.nrttools.SessionObject import SessionObject


class Bus(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buses',
        '_calculation_rate',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        bus_count=1,
        calculation_rate=None,
        ):
        from supriya.tools import nrttools
        SessionObject.__init__(self, session)
        assert calculation_rate is not None
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            nrttools.Bus(
                session,
                bus_group=self,
                calculation_rate=self.calculation_rate,
                )
            for _ in range(bus_count)
            )

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return self.buses.__contains__(item)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buses[item]
        elif isinstance(item, slice):
            indices = item.indices(len(self))
            bus_count = indices[1] - indices[0]
            bus_group = type(self)(
                self.session,
                bus_count=bus_count,
                calculation_rate=self.calculation_rate,
                )
            return bus_group

    def __iter__(self):
        return iter(self.buses)

    def __len__(self):
        return len(self._buses)

    ### PUBLIC METHODS ###

    def fill(self, value):
        pass

    def get_map_symbol(self, bus_id):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(bus_id)
        return map_symbol

    def index(self, item):
        return self.buses.index(item)

    ### PUBLIC PROPERTIES ###

    @property
    def buses(self):
        return self._buses

    @property
    def calculation_rate(self):
        return self._calculation_rate
