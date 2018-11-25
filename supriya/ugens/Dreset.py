import collections

from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dreset(DUGen):
    """
    Resets demand-rate UGens.

    ::

        >>> source = supriya.ugens.Dseries(start=0, step=2)
        >>> dreset = supriya.ugens.Dreset(
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> dreset
        Dreset()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("source", None), ("reset", 0)])

    _valid_calculation_rates = (CalculationRate.DEMAND,)
