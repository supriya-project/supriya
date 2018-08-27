import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dbufwr(DUGen):
    """
    A buffer-writing demand-rate UGen.

    ::

        >>> dbufwr = supriya.ugens.Dbufwr(
        ...     buffer_id=0,
        ...     source=0,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> dbufwr
        Dbufwr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Demand UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', 0.0),
        ('buffer_id', 0.0),
        ('phase', 0.0),
        ('loop', 1.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.DEMAND,
    )
