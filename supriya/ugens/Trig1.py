import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Trig1(UGen):
    """
    A timed trigger.

    ::

        >>> source = supriya.ugens.Dust.kr(1)
        >>> trig_1 = supriya.ugens.Trig1.ar(
        ...     duration=0.1,
        ...     source=source,
        ...     )
        >>> trig_1
        Trig1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('duration', 0.1),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
