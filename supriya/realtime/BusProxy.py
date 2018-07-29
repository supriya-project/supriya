from supriya.system.SupriyaValueObject import SupriyaValueObject


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
        value=0.0,
    ):
        import supriya.realtime
        import supriya.synthdefs
        bus_id = int(bus_id)
        assert 0 <= bus_id
        calculation_rate = supriya.CalculationRate.from_expr(
            calculation_rate)
        assert isinstance(server, supriya.realtime.Server)
        self._bus_id = int(bus_id)
        self._calculation_rate = calculation_rate
        self._server = server
        self._value = value or 0.0

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
        import supriya.synthdefs
        if self.calculation_rate == supriya.CalculationRate.AUDIO:
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
