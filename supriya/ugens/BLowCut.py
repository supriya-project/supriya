import collections
from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BLowCut(BEQSuite):
    """
    A low-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_cut = supriya.ugens.BLowCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ...     )
        >>> blow_cut
        BLowCut.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('frequency', 1200), ('order', 2), ('max_order', 5)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
