# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BusProxy(SupriyaObject):
    r'''A buffer proxy.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_bus_id',
        '_calculation_rate',
        '_server',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_id=None,
        rate=None,
        server=None,
        value=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        bus_id = int(bus_id)
        assert 0 <= bus_id
        rate = synthdeftools.CalculationRate.from_expr(
            rate)
        assert isinstance(server, servertools.Server)
        self._bus_id = int(bus_id)
        self._calculation_rate = rate
        self._server = server
        self._value = None

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

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def rate(self):
        return self._calculation_rate

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        if self.rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(self.bus_id)
        return map_symbol

    @property
    def server(self):
        return self._server

    @property
    def value(self):
        return self._value