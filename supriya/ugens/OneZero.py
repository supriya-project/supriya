import collections
from supriya.enums import CalculationRate
from supriya.ugens.OnePole import OnePole


class OneZero(OnePole):
    """
    A one zero filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> one_zero = supriya.ugens.OneZero.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ...     )
        >>> one_zero
        OneZero.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 0.5)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
