import collections

from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dxrand(DUGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dxrand = supriya.ugens.Dxrand.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> dxrand
        Dxrand()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("repeats", 1), ("sequence", None)])

    _unexpanded_input_names = ("sequence",)

    _valid_calculation_rates = (CalculationRate.DEMAND,)
