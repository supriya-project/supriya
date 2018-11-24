import collections
from supriya import CalculationRate
from supriya.ugens.Dwhite import Dwhite


class Diwhite(Dwhite):
    """
    An integer demand-rate white noise random generator.

    ::

        >>> diwhite = supriya.ugens.Diwhite.new(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     )
        >>> diwhite
        Diwhite()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('minimum', 0), ('maximum', 1), ('length', float('inf'))]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
