import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Trig(UGen):
    """
    A timed trigger.

    ::

        >>> source = supriya.ugens.Dust.kr(1)
        >>> trig = supriya.ugens.Trig.ar(
        ...     duration=0.1,
        ...     source=source,
        ...     )
        >>> trig
        Trig.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('duration', 0.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
