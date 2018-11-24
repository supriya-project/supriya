import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class QuadN(UGen):
    """
    A non-interpolating general quadratic map chaotic generator.

    ::

        >>> quad_n = supriya.ugens.QuadN.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> quad_n
        QuadN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1), ("b", -1), ("c", -0.75), ("xi", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
