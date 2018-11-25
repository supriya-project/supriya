import collections

from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dbrown(DUGen):
    """
    A demand-rate brownian movement generator.

    ::

        >>> dbrown = supriya.ugens.Dbrown.new(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ...     )
        >>> dbrown
        Dbrown()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Demand UGens"

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("step", 0.01), ("length", float("inf"))]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
