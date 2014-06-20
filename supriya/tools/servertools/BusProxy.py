# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BusProxy(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_id'
        '_calculation_rate',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_id=None,
        calculation_rate=None,
        server=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        bus_id = int(bus_id)
        assert 0 <= bus_id
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        assert isinstance(server, servertools.Server)
        self._bus_id = int(bus_id)
        self._calculation_rate = calculation_rate
        self._server = server

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __float__(self):
        return float(self.bus_id)

    def __hash__(self):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __int__(self):
        return int(self.bus_id)

    def __str__(self):
        return self.map_symbol

    ### PUBLIC METHODS ###

    def handle_response(self, response):
        from supriya.tools import responsetools
        assert response.buffer_id == self.buffer_id
        if isinstance(response, responsetools.ControlBusSetContiguousResponse):
            pass
        elif isinstance(response, responsetools.ControlBusSetResponse):
            pass

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(self.bus_id)
        return map_symbol

    @property
    def server(self):
        return self._server
