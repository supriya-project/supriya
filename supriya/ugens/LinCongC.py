import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LinCongC(UGen):
    """
    A cubic-interpolating linear congruential chaotic generator.

    ::

        >>> lin_cong_c = supriya.ugens.LinCongC.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ...     )
        >>> lin_cong_c
        LinCongC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.1), ("c", 0.13), ("m", 1), ("xi", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
