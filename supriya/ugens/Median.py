import collections

from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Median(Filter):
    """
    A median filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> median = supriya.ugens.Median.ar(
        ...     length=3,
        ...     source=source,
        ...     )
        >>> median
        Median.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict([("length", 3), ("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
