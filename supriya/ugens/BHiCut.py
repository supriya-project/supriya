import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BHiCut(BEQSuite):
    """
    A high-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_cut = supriya.ugens.BHiCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ...     )
        >>> bhi_cut
        BHiCut.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('frequency', 1200),
        ('order', 2),
        ('max_order', 5),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
