import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dseries(DUGen):
    """
    A demand-rate arithmetic series.

    ::

        >>> dseries = supriya.ugens.Dseries.new(
        ...     length=float('inf'),
        ...     start=1,
        ...     step=1,
        ...     )
        >>> dseries
        Dseries()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('start', 1),
        ('step', 1),
        ('length', float('inf')),
    ])

    _valid_calculation_rates = (
        CalculationRate.DEMAND,
    )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        length=float('inf'),
        start=1,
        step=1,
    ):
        if length is None:
            length = float('inf')
        DUGen.__init__(
            self,
            length=length,
            start=start,
            step=step,
            )
