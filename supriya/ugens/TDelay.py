import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class TDelay(UGen):
    """
    A trigger delay.

    ::

        >>> source = supriya.ugens.Dust.kr()
        >>> tdelay = supriya.ugens.TDelay.ar(
        ...     duration=0.1,
        ...     source=source,
        ...     )
        >>> tdelay
        TDelay.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("duration", 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
