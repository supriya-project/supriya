import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Latch(UGen):
    """
    Samples and holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> latch = supriya.ugens.Latch.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> latch
        Latch.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict([('source', None), ('trigger', 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
