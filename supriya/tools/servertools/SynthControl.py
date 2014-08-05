# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControl(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        '_default_value',
        '_name',
        '_range',
        '_rate',
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        name=None,
        range_=None,
        rate=None,
        unit=None,
        value=None,
        ):
        from supriya.tools import synthdeftools
        self._client = client
        self._name = str(name)
        if isinstance(range_, synthdeftools.Range):
            self._range = range_
        else:
            self._range = None
        self._rate = synthdeftools.Rate.from_expr(rate)
        self._unit = unit
        self._value = value
        self._default_value = value

    ### SPECIAL METHODS ###

    def __str__(self):
        return self.name

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'name',
                'range_',
                'rate',
                'unit',
                'value',
                ),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_parameter(cls, parameter, client=None):
        from supriya.tools import synthdeftools
        assert isinstance(parameter, synthdeftools.Parameter)
        name = parameter.name
        range_ = parameter.range_
        rate = synthdeftools.Rate.from_input(parameter)
        unit = parameter.unit
        value = parameter.value
        synth_control = SynthControl(
            client=client,
            name=name,
            range_=range_,
            rate=rate,
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
            self._value = expr
            if expr.rate == synthdeftools.Rate.CONTROL:
                request = requesttools.NodeMapToControlBusRequest(
                    self.synth,
                    **{self.name: self._value}
                    )
            else:
                request = requesttools.NodeMapToAudioBusRequest(
                    self.synth,
                    **{self.name: self._value}
                    )
        else:
            self._value = float(expr)
            request = requesttools.NodeSetRequest(
                self.synth,
                **{self.name: self._value}
                )
        if self.synth.is_allocated:
            request.communicate(server=self.synth.server)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def default_value(self):
        return self._default_value

    @property
    def name(self):
        return self._name

    @property
    def range_(self):
        return self._range

    @property
    def rate(self):
        return self._rate

    @property
    def synth(self):
        return self.client.client

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value