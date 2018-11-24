import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class ToggleFF(UGen):
    """
    A toggle flip-flop.

    ::

        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> toggle_ff = supriya.ugens.ToggleFF.ar(
        ...     trigger=trigger,
        ...     )
        >>> toggle_ff
        ToggleFF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict([('trigger', 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
