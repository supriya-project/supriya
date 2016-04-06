# -*- encoding: utf-8 -*-
from supriya.tools.bindingtools.BindingTarget import BindingTarget


class SynthControl(BindingTarget):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_binding_sources',
        '_calculation_rate',
        '_client',
        '_index',
        '_default_value',
        '_last_unmapped_value',
        '_name',
        '_range',
        '_unit',
        '_value',
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
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        BindingTarget.__init__(self)
        self._client = client
        self._name = str(name)
        if isinstance(range_, synthdeftools.Range):
            self._range = range_
        else:
            self._range = None
        self._calculation_rate = synthdeftools.CalculationRate.from_expr(calculation_rate)
        self._unit = unit
        self._value = value
        self._default_value = value
        if not isinstance(value, servertools.Bus):
            self._last_unmapped_value = self._value
        else:
            self._last_unmapped_value = self._default_value
        if index is not None:
            index = int(index)
        self._index = index

    ### SPECIAL METHODS ###

    def __str__(self):
        return self.name

    ### PRIVATE METHODS ###

    def _map_to_bus(self, bus):
        from supriya.tools import servertools
        if not isinstance(self.value, servertools.Bus):
            self._last_unmapped_value = self._value
        self._value = bus

    def _receive_bound_event(self, event=None):
        if event is None:
            return
        event = float(event)
        self.set(event)

    def _set_to_number(self, value):
        self._value = float(value)
        self._last_unmapped_value = self._value

    def _unmap(self):
        self._value = self._last_unmapped_value

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'name',
                'range_',
                'calculation_rate',
                'unit',
                'value',
                ),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_parameter(
        cls,
        parameter,
        index=0,
        client=None,
        ):
        from supriya.tools import synthdeftools
        assert isinstance(parameter, synthdeftools.Parameter)
        name = parameter.name
        range_ = parameter.range_
        calculation_rate = synthdeftools.CalculationRate.from_input(parameter)
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
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        if isinstance(expr, servertools.Bus):
            self._map_to_bus(expr)
            if expr.calculation_rate == synthdeftools.CalculationRate.CONTROL:
                request = requesttools.NodeMapToControlBusRequest(
                    self.node,
                    **{self.name: self._value}
                    )
            else:
                request = requesttools.NodeMapToAudioBusRequest(
                    self.node,
                    **{self.name: self._value}
                    )
        elif expr is None:
            self._unmap()
            request = requesttools.NodeMapToControlBusRequest(
                self.node,
                **{self.name: -1}
                )
        else:
            self._set_to_number(expr)
            request = requesttools.NodeSetRequest(
                self.node,
                **{self.name: self._value}
                )
        if self.node.is_allocated:
            request.communicate(server=self.node.server)

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
