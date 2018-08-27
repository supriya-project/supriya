import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BLowShelf(BEQSuite):
    """
    A low-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_shelf = supriya.ugens.BLowShelf.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ...     )
        >>> blow_shelf
        BLowShelf.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('frequency', 1200),
        ('reciprocal_of_s', 1),
        ('gain', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
