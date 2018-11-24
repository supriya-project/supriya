import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dseq(DUGen):
    """
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dseq = supriya.ugens.Dseq.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> dseq
        Dseq()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([('repeats', 1), ('sequence', None)])

    _unexpanded_input_names = ('sequence',)

    _valid_calculation_rates = (CalculationRate.DEMAND,)
