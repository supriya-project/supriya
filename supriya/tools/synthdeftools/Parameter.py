# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class Parameter(UGenMethodMixin):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_name',
        '_parameter_rate',
        '_range',
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        parameter_rate=None,
        range_=None,
        unit=None,
        value=None,
        ):
        from supriya.tools import synthdeftools
        assert name
        self._name = str(name)
        self._parameter_rate = synthdeftools.ParameterRate.from_expr(parameter_rate)
        if range_ is not None:
            assert isinstance(range_, synthdeftools.Range)
        self._range = range_
        self._unit = unit
        self._value = float(value)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        elif self.name != expr.name:
            return False
        elif self.parameter_rate != expr.parameter_rate:
            return False
        return True

    def __getitem__(self, i):
        return self

    def __hash__(self):
        hash_values = (
            type(self),
            self.name,
            self.parameter_rate,
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
    def has_done_flag(self):
        return False

    @property
    def name(self):
        return self._name

    @property
    def parameter_rate(self):
        return self._parameter_rate

    @property
    def range_(self):
        return self._range

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value