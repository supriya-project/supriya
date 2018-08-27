import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Logistic(UGen):
    """
    A chaotic noise function.

    ::

        >>> logistic = supriya.ugens.Logistic.ar(
        ...     chaos_parameter=3.,
        ...     frequency=1000,
        ...     initial_y=0.5,
        ...     )
        >>> logistic
        Logistic.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    _ordered_input_names = collections.OrderedDict([
        ('chaos_parameter', 3),
        ('frequency', 1000),
        ('initial_y', 0.5),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
