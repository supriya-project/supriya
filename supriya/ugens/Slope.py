import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Slope(Filter):
    """
    Calculates slope of signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slope = supriya.ugens.Slope.ar(
        ...     source=source,
        ...     )
        >>> slope
        Slope.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
