import collections
from supriya import CalculationRate
from supriya.ugens.Dbrown import Dbrown


class Dibrown(Dbrown):
    """
    An integer demand-rate brownian movement generator.

    ::

        >>> dibrown = supriya.ugens.Dibrown.new(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ...     )
        >>> dibrown
        Dibrown()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('minimum', 0), ('maximum', 12), ('step', 1), ('length', float('inf'))]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
