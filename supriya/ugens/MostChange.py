import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class MostChange(UGen):
    """
    Outputs most changed input.

    ::

        >>> most_change = supriya.ugens.MostChange.ar(
        ...     a=0,
        ...     b=0,
        ...     )
        >>> most_change
        MostChange.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('a', 0),
        ('b', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
