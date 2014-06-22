# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControl(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_rate',
        '_range',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        value=None,
        range_=None,
        rate=None,
        ):
        self._name = str(name)
        self.value = value
        self._range = servertools.Range(range_)
        self._rate = synthdeftools.Rate.from_expr(rate)

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
    def value(self):
        return self._value

    @value.setter
    def value(self, expr):
        if isinstance(expr, servertools.Bus):
            self._value = expr
        else:
            self._value = float(expr)
