# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class Parameter(UGenMethodMixin):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_control_rate',
        '_name',
        '_range',
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        control_rate=None,
        name=None,
        range_=None,
        unit=None,
        value=None,
        ):
        from supriya.tools import synthdeftools
        assert name
        self._control_rate = synthdeftools.ControlRate.from_expr(control_rate)
        self._name = str(name)
        self._range = synthdeftools.Range(range_)
        self._unit = unit
        self._value = float(value)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        elif self.name != expr.name:
            return False
        elif self.control_rate != expr.control_rate:
            return False
        return True

    def __getitem__(self, i):
        return self

    def __hash__(self):
        hash_values = (
            type(self),
            self.control_rate,
            self.name,
            )
        return hash(hash_values)

    def __len__(self):
        return 1

    ### PRIVATE METHODS ###

    def _get_source(self):
        return self

    def _get_output_number(self):
        return 0

    ### PUBLIC PROPERTIES ###

    @property
    def control_rate(self):
        return self._control_rate

    @property
    def name(self):
        return self._name

    @property
    def range_(self):
        return self._range

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value
