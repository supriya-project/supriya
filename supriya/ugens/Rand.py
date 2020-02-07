import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Rand(UGen):
    """
    A uniform random distribution.

    ::

        >>> supriya.ugens.Rand.ir()
        Rand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("minimum", 0.0), ("maximum", 1.0)])

    _valid_calculation_rates = (CalculationRate.SCALAR,)
