import collections

from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Slew(Filter):
    """
    A slew rate limiter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slew = supriya.ugens.Slew.ar(
        ...     source=source,
        ...     up=1,
        ...     down=1,
        ...     )
        >>> slew
        Slew.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("up", 1), ("down", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
