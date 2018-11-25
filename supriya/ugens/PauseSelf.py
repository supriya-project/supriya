import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class PauseSelf(UGen):
    """
    Pauses the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause_self = supriya.ugens.PauseSelf.kr(
        ...     trigger=trigger,
        ...     )
        >>> pause_self
        PauseSelf.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Envelope Utility UGens"

    _ordered_input_names = collections.OrderedDict([("trigger", None)])

    _valid_calculation_rates = (CalculationRate.CONTROL,)
