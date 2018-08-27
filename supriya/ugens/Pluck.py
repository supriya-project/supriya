import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Pluck(UGen):
    """
    A Karplus-String UGen.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(2)
        >>> pluck = supriya.ugens.Pluck.ar(
        ...     coefficient=0.5,
        ...     decay_time=1,
        ...     delay_time=0.2,
        ...     maximum_delay_time=0.2,
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> pluck
        Pluck.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('trigger', None),
        ('maximum_delay_time', 0.2),
        ('delay_time', 0.2),
        ('decay_time', 1),
        ('coefficient', 0.5),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
