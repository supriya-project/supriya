import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Peak(UGen):
    """
    Tracks peak signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> peak = supriya.ugens.Peak.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> peak
        Peak.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
