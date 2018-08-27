import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Limiter(UGen):
    """
    A peak limiter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> limiter = supriya.ugens.Limiter.ar(
        ...     duration=0.01,
        ...     level=1,
        ...     source=source,
        ...     )
        >>> limiter
        Limiter.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Dynamics UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('level', 1),
        ('duration', 0.01),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
