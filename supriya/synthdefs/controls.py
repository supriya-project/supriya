import collections
from collections.abc import Sequence

from supriya import CalculationRate, ParameterRate, SignalRange
from supriya.system import SupriyaValueObject
from supriya.typing import UGenInputMap

from .bases import MultiOutUGen
from .mixins import UGenMethodMixin


class Range(SupriyaValueObject):
    """
    A range.

    ::

        >>> supriya.synthdefs.Range(-1.0, 1.0)
        Range(
            maximum=1.0,
            minimum=-1.0,
        )

    ::

        >>> supriya.synthdefs.Range(minimum=0.0)
        Range(
            maximum=inf,
            minimum=0.0,
        )

    ::

        >>> supriya.synthdefs.Range()
        Range(
            maximum=inf,
            minimum=-inf,
        )

    ::

        >>> supriya.synthdefs.Range((0.1, 0.9))
        Range(
            maximum=0.9,
            minimum=0.1,
        )

    ::

        >>> supriya.synthdefs.Range(supriya.synthdefs.Range(-3, 3))
        Range(
            maximum=3.0,
            minimum=-3.0,
        )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_minimum", "_maximum")

    ### INITIALIZER ###

    def __init__(self, minimum=None, maximum=None):
        if isinstance(minimum, Sequence) and maximum is None and len(minimum) == 2:
            minimum, maximum = minimum
        elif isinstance(minimum, type(self)):
            minimum, maximum = minimum.minimum, minimum.maximum
        if minimum is None:
            minimum = float("-inf")
        if not isinstance(minimum, (float, int)):
            raise ValueError(minimum)
        minimum = float(minimum)
        if maximum is None:
            maximum = float("inf")
        if not isinstance(maximum, (float, int)):
            raise ValueError(maximum)
        maximum = float(maximum)
        assert minimum <= maximum
        self._minimum = minimum
        self._maximum = maximum

    ### PUBLIC METHODS ###

    @staticmethod
    def scale(value, input_range, output_range, exponent=1.0):
        """
        Scales `value` from `input_range` to `output_range`.

        Curve value exponentially by `exponent`.

        ::

            >>> input_range = supriya.synthdefs.Range(0.0, 10.0)
            >>> output_range = supriya.synthdefs.Range(-2.5, 2.5)

        ::

            >>> supriya.synthdefs.Range.scale(0.0, input_range, output_range)
            -2.5

        ::

            >>> supriya.synthdefs.Range.scale(5.0, input_range, output_range)
            0.0

        ::

            >>> supriya.synthdefs.Range.scale(5.0, input_range, output_range, 2.0)
            -1.25

        ::

            >>> supriya.synthdefs.Range.scale(5.0, input_range, output_range, 0.5)
            1.0355...

        Returns float.
        """
        value = (value - input_range.minimum) / input_range.width
        if exponent != 1:
            value = pow(value, exponent)
        value = (value * output_range.width) + output_range.minimum
        return value

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        return self._maximum

    @property
    def minimum(self):
        return self._minimum

    @property
    def width(self):
        return self._maximum - self._minimum


class Parameter(UGenMethodMixin, SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        "_lag",
        "_name",
        "_parameter_rate",
        "_range",
        "_unit",
        "_uuid",
        "_value",
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
        if lag is not None:
            lag = float(lag)
        self._lag = lag
        if name is not None:
            name = str(name)
        self._name = name
        self._parameter_rate = ParameterRate.from_expr(parameter_rate)
        if range_ is not None:
            assert isinstance(range_, Range)
        self._range = range_
        self._unit = unit
        self._uuid = None
        if isinstance(value, Sequence):
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
        return CalculationRate.from_expr(self)

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
    def signal_range(self):
        SignalRange.BIPOLAR

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value


class Control(MultiOutUGen):
    """
    A control-rate control ugen.

    Control ugens can be set and routed externally to interact with a running
    synth. Controls are created from the parameters of a synthesizer
    definition, and typically do not need to be created by hand.
    """

    ### CLASS VARIABLES ###

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    __slots__ = ("_parameters",)

    ### INITIALIZER ###

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        coerced_parameters = []
        for parameter in parameters:
            if not isinstance(parameter, Parameter):
                parameter = Parameter(name=parameter, value=0)
            coerced_parameters.append(parameter)
        self._parameters = tuple(coerced_parameters)
        MultiOutUGen.__init__(
            self,
            channel_count=len(self),
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
        )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets output proxy at `i`, via index or control name.

        Returns output proxy.
        """
        import supriya.synthdefs

        if type(i) == int:
            if len(self) == 1:
                return supriya.synthdefs.OutputProxy(self, 0)
            return supriya.synthdefs.OutputProxy(self, i)
        else:
            return self[self._get_control_index(i)]

    def __len__(self):
        """
        Gets number of ugen outputs.

        Equal to the number of control names.

        Returns integer.
        """
        return sum(len(_) for _ in self.parameters)

    ### PRIVATE METHODS ###

    def _get_control_index(self, control_name):
        for i, parameter in enumerate(self._parameters):
            if parameter.name == control_name:
                return i
        raise ValueError

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    def _get_parameter_output_proxies(self):
        output_proxies = []
        for parameter in self.parameters:
            output_proxies.extend(parameter)
        return output_proxies

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        """
        Gets controls of control ugen.

        Returns ugen graph.
        """
        import supriya.synthdefs

        if len(self.parameters) == 1:
            result = self
        else:
            result = [
                supriya.synthdefs.OutputProxy(self, i)
                for i in range(len(self.parameters))
            ]
        return result

    @property
    def parameters(self):
        """
        Gets control names associated with control.

        Returns tuple.
        """
        return self._parameters

    @property
    def starting_control_index(self):
        """
        Gets starting control index of control ugen.

        Equivalent to the control ugen's special index.

        Returns integer.
        """
        return self._special_index


class AudioControl(Control):
    """
    A trigger-rate control ugen.
    """

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        Control.__init__(
            self,
            parameters,
            calculation_rate=CalculationRate.AUDIO,
            starting_control_index=starting_control_index,
        )


class LagControl(Control):
    """
    A lagged control-rate control ugen.
    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("lags", None)])

    _unexpanded_input_names = ("lags",)

    ### INITIALIZER ###

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        coerced_parameters = []
        for parameter in parameters:
            if not isinstance(parameter, Parameter):
                parameter = Parameter(name=parameter, value=0)
            coerced_parameters.append(parameter)
        self._parameters = tuple(coerced_parameters)
        lags = []
        for parameter in self._parameters:
            lag = parameter.lag or 0.0
            lags.extend([lag] * len(parameter))
        MultiOutUGen.__init__(
            self,
            channel_count=len(self),
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
            lags=lags,
        )


class TrigControl(Control):
    """
    A trigger-rate control ugen.
    """

    ### CLASS VARIABLES ###

    ### INITIALIZER ##

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        Control.__init__(
            self,
            parameters,
            calculation_rate=CalculationRate.CONTROL,
            starting_control_index=starting_control_index,
        )
