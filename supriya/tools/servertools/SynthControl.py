# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControl(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_value',
        '_name',
        '_rate',
        '_range',
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        range_=None,
        rate=None,
        unit=None,
        value=None,
        ):
        from supriya.tools import synthdeftools
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

    ### PUBLIC METHODS ###

    @classmethod
    def from_parameter(cls, parameter):
        from supriya.tools import synthdeftools
        assert isinstance(parameter, synthdeftools.Parameter)
        name = parameter.name
        range_ = parameter.range_
        rate = synthdeftools.Rate.from_input(parameter)
        unit = parameter.unit
        value = parameter.value
        synth_control = SynthControl(
            name=name,
            range_=range_,
            rate=rate,
            unit=unit,
            value=value,
            )
        return synth_control

    def reset(self):
        self._value = self._default_value

    ### PUBLIC PROPERTIES ###

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
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, expr):
        from supriya.tools import servertools
        if isinstance(expr, servertools.Bus):
            assert expr.rate == self.rate
            self._value = expr
        else:
            self._value = float(expr)
