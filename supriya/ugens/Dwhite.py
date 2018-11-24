import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dwhite(DUGen):
    """
    A demand-rate white noise random generator.

    ::

        >>> dwhite = supriya.ugens.Dwhite.new(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     )
        >>> dwhite
        Dwhite()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("length", float("inf"))]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
