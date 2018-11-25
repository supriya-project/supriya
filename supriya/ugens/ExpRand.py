import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class ExpRand(UGen):
    """
    An exponential random distribution.

    ::

        >>> exp_rand = supriya.ugens.ExpRand.ir()
        >>> exp_rand
        ExpRand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("minimum", 0.0), ("maximum", 1.0)])

    _valid_calculation_rates = (CalculationRate.SCALAR,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, maximum=None, minimum=None):
        minimum, maximum = sorted([minimum, maximum])
        UGen.__init__(
            self, calculation_rate=calculation_rate, minimum=minimum, maximum=maximum
        )
