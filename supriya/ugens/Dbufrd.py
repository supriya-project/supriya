import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dbufrd(DUGen):
    """
    A buffer-reading demand-rate UGen.

    ::

        >>> dbufrd = supriya.ugens.Dbufrd(
        ...     buffer_id=0,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> dbufrd
        Dbufrd()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Demand UGens"

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", 0), ("phase", 0), ("loop", 1)]
    )

    _valid_calculation_rates = (CalculationRate.DEMAND,)
