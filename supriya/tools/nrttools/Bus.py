# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools.nrttools.SessionObject import SessionObject


class Bus(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_group',
        '_calculation_rate',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        bus_group=None,
        calculation_rate=None,
        ):
        from supriya.tools import nrttools
        SessionObject.__init__(self, session)
        if bus_group is not None:
            assert isinstance(bus_group, nrttools.BusGroup)
        self._bus_group = bus_group
        assert calculation_rate is not None
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate

    ### PUBLIC METHODS ###

    def get_map_symbol(self, bus_id):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(bus_id)
        return map_symbol

    def set(self, value):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self):
        return self._bus_group

    @property
    def calculation_rate(self):
        return self._calculation_rate
