import collections
from supriya.enums import CalculationRate
from supriya.ugens.MostChange import MostChange


class LeastChange(MostChange):
    """
    Outputs least changed input.

    ::

        >>> least_change = supriya.ugens.LeastChange.ar(
        ...     a=0,
        ...     b=0,
        ...     )
        >>> least_change
        LeastChange.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([('a', 0), ('b', 0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
