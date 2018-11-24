import collections
from supriya import CalculationRate
from supriya.ugens.Peak import Peak


class RunningMin(Peak):
    """
    Tracks minimum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> running_min = supriya.ugens.RunningMin.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> running_min
        RunningMin.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict([('source', None), ('trigger', 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
