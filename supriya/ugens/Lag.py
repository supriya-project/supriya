import collections

from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Lag(Filter):
    """
    A lag generator.

    ::

        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.Lag.kr(
        ...     lag_time=0.5,
        ...     source=source,
        ...     )
        Lag.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time", 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
