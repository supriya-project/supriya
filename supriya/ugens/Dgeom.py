import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dgeom(DUGen):
    """
    A demand-rate geometric series generator.

    ::

        >>> dgeom = supriya.ugens.Dgeom.new(
        ...     grow=2,
        ...     length=float('inf'),
        ...     start=1,
        ...     )
        >>> dgeom
        Dgeom()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('start', 1), ('grow', 2), ('length', float('inf'))]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
