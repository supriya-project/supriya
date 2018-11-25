import collections

from supriya import CalculationRate
from supriya.ugens.BEQSuite import BEQSuite


class BHiShelf(BEQSuite):
    """
    A high-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
        ...     gain=0,
        ...     frequency=1200,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ...     )
        >>> bhi_shelf
        BHiShelf.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_s", 1), ("gain", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
