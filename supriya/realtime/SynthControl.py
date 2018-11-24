from supriya.system.Bindable import Bindable


class SynthControl:

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_calculation_rate',
        '_client',
        '_index',
        '_default_value',
        '_last_unmapped_value',
        '_name',
        '_range',
        '_unit',
        '_value',
        '__weakref__',
    )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        index=None,
        name=None,
        range_=None,
        calculation_rate=None,
        unit=None,
        value=None,
    ):
        import supriya.realtime
        import supriya.synthdefs

        self._client = client
        self._name = str(name)
        if isinstance(range_, supriya.synthdefs.Range):
            self._range = range_
        else:
            self._range = None
        self._calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        self._unit = unit
        self._value = value
        self._default_value = value
        if not isinstance(value, supriya.realtime.Bus):
            self._last_unmapped_value = self._value
        else:
            self._last_unmapped_value = self._default_value
        if index is not None:
            index = int(index)
        self._index = index

    ### SPECIAL METHODS ###

    @Bindable(rebroadcast=False)
    def __call__(self, expr):
        return self.set(expr)

    def __str__(self):
        return self.name

    ### PRIVATE METHODS ###

    def _map_to_bus(self, bus):
        import supriya.realtime

        if not isinstance(self.value, supriya.realtime.Bus):
            self._last_unmapped_value = self._value
        self._value = bus

    def _set_to_number(self, value):
        self._value = float(value)
        self._last_unmapped_value = self._value

    def _unmap(self):
        self._value = self._last_unmapped_value

    ### PUBLIC METHODS ###

    @classmethod
    def from_parameter(cls, parameter, index=0, client=None):
        import supriya.synthdefs

        assert isinstance(parameter, supriya.synthdefs.Parameter)
        name = parameter.name
        range_ = parameter.range_
        calculation_rate = supriya.CalculationRate.from_expr(parameter)
        unit = parameter.unit
        value = parameter.value
        synth_control = SynthControl(
            client=client,
            index=index,
            name=name,
            range_=range_,
            calculation_rate=calculation_rate,
            unit=unit,
            value=value,
        )
        return synth_control

    def get(self):
        return self._value

    def reset(self):
        self._value = self._default_value

    def set(self, expr):
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs

        if isinstance(expr, supriya.realtime.Bus):
            self._map_to_bus(expr)
            if expr.calculation_rate == supriya.CalculationRate.CONTROL:
                request = supriya.commands.NodeMapToControlBusRequest(
                    self.node, **{self.name: self._value}
                )
            else:
                request = supriya.commands.NodeMapToAudioBusRequest(
                    self.node, **{self.name: self._value}
                )
        elif expr is None:
            self._unmap()
            request = supriya.commands.NodeMapToControlBusRequest(
                self.node, **{self.name: -1}
            )
        else:
            self._set_to_number(expr)
            request = supriya.commands.NodeSetRequest(
                self.node, **{self.name: self._value}
            )
        if self.node.is_allocated:
            request.communicate(server=self.node.server)
        return self.get()

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def client(self):
        return self._client

    @property
    def default_value(self):
        return self._default_value

    @property
    def index(self):
        return self._index

    @property
    def last_unmapped_value(self):
        return self._last_unmapped_value

    @property
    def name(self):
        return self._name

    @property
    def range_(self):
        return self._range

    @property
    def node(self):
        return self.client.client

    @property
    def synth(self):
        return self.client.client

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value
