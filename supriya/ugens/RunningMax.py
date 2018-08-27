import collections
from supriya import CalculationRate
from supriya.ugens.Peak import Peak


class RunningMax(Peak):
    """
    Tracks maximum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> running_max = supriya.ugens.RunningMax.ar(
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> running_max
        RunningMax.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('trigger', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
