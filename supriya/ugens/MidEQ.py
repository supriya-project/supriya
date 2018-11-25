import collections

from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class MidEQ(Filter):
    """
    A parametric filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> mid_eq = supriya.ugens.MidEQ.ar(
        ...     db=0,
        ...     frequency=440,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ...     )
        >>> mid_eq
        MidEQ.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("reciprocal_of_q", 1), ("db", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
