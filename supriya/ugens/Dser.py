import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dser(DUGen):
    """
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dser = supriya.ugens.Dser.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> dser
        Dser()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([('repeats', 1), ('sequence', None)])

    _unexpanded_input_names = ('sequence',)

    _valid_calculation_rates = (CalculationRate.DEMAND,)
