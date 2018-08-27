import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dstutter(DUGen):
    """
    A demand-rate input replicator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> dstutter = supriya.ugens.Dstutter.new(
        ...     n=2,
        ...     source=source,
        ...     )
        >>> dstutter
        Dstutter()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('n', 2.0),
        ('source', None),
    ])

    _valid_calculation_rates = (
        CalculationRate.DEMAND,
    )
