from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class BusProxy(SupriyaValueObject):
    """
    A buffer proxy.
    """

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
        calculation_rate=None,
        server=None,
        value=None,
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
        self._value = None

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.bus_id)

    def __int__(self):
        return int(self.bus_id)

    def __str__(self):
        return self.map_symbol

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

    @property
    def value(self):
        return self._value
