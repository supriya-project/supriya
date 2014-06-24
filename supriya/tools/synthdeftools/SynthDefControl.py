# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class SynthDefControl(UGenMethodMixin):

    ### CLASS VARIABLES ###

    __slots__ = (
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
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        self._name = str(name)
        self._range = servertools.Range(range_)
        self._rate = synthdeftools.Rate.from_expr(rate)
        self._unit = unit
        self._value = float(value)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self

    def __len__(self):
        return 1

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
