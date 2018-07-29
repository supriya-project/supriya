import collections
from supriya.synthdefs.ParameterRate import ParameterRate
from supriya.synthdefs.UGenMethodMixin import UGenMethodMixin
from supriya.system.SupriyaValueObject import SupriyaValueObject


class Parameter(UGenMethodMixin, SupriyaValueObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_lag',
        '_name',
        '_parameter_rate',
        '_range',
        '_unit',
        '_uuid',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lag=None,
        name=None,
        parameter_rate=ParameterRate.CONTROL,
        range_=None,
        unit=None,
        value=None,
        ):
        import supriya.synthdefs
        #assert name
        if lag is not None:
            lag = float(lag)
        self._lag = lag
        if name is not None:
            name = str(name)
        self._name = name
        self._parameter_rate = supriya.synthdefs.ParameterRate.from_expr(
            parameter_rate)
        if range_ is not None:
            assert isinstance(range_, supriya.synthdefs.Range)
        self._range = range_
        self._unit = unit
        self._uuid = None
        if isinstance(value, collections.Sequence):
            value = tuple(float(_) for _ in value)
            assert value, value
        else:
            value = float(value)
        self._value = value

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self._get_output_proxy(i)

    def __len__(self):
        if isinstance(self.value, float):
            return 1
        return len(self.value)

    ### PRIVATE METHODS ###

    def _get_source(self):
        return self

    def _get_output_number(self):
        return 0

    def _optimize_graph(self, sort_bundles):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        import supriya.synthdefs
        return supriya.CalculationRate.from_input(self)

    @property
    def has_done_flag(self):
        return False

    @property
    def inputs(self):
        return ()

    @property
    def lag(self):
        return self._lag

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
