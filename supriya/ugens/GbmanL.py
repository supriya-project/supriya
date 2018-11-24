import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class GbmanL(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.

    ::

        >>> gbman_l = supriya.ugens.GbmanL.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ...     )
        >>> gbman_l
        GbmanL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("xi", 1.2), ("yi", 2.1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
