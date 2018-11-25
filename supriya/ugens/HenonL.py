import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class HenonL(UGen):
    """
    A linear-interpolating henon map chaotic generator.

    ::

        >>> henon_l = supriya.ugens.HenonL.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ...     )
        >>> henon_l
        HenonL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.4), ("b", 0.3), ("x_0", 0), ("x_1", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
