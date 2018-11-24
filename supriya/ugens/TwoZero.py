import collections

from supriya import CalculationRate
from supriya.ugens.TwoPole import TwoPole


class TwoZero(TwoPole):
    """
    A two zero filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_zero = supriya.ugens.TwoZero.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> two_zero
        TwoZero.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("radius", 0.8)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
