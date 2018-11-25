import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Gate(UGen):
    """
    Gates or holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> gate = supriya.ugens.Gate.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> gate
        Gate.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
