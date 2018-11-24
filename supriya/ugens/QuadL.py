import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class QuadL(UGen):
    """
    A linear-interpolating general quadratic map chaotic generator.

    ::

        >>> quad_l = supriya.ugens.QuadL.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> quad_l
        QuadL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1), ("b", -1), ("c", -0.75), ("xi", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
