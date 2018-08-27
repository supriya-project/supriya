import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Decay2(Filter):
    """
    A leaky signal integrator.

    ::

        >>> source = supriya.ugens.Impulse.ar()
        >>> decay_2 = supriya.ugens.Decay2.ar(
        ...     source=source,
        ...     )
        >>> decay_2
        Decay2.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('attack_time', 0.01),
        ('decay_time', 1.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
