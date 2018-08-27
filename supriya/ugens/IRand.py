import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class IRand(UGen):
    """
    An integer uniform random distribution.

    ::

        >>> supriya.ugens.IRand.ir()
        IRand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    _ordered_input_names = collections.OrderedDict([
        ('minimum', 0),
        ('maximum', 127),
    ])

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
    )
