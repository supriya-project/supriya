import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class CuspN(UGen):
    """
    A non-interpolating cusp map chaotic generator.

    ::

        >>> cusp_n = supriya.ugens.CuspN.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> cusp_n
        CuspN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 22050), ("a", 1.0), ("b", 1.9), ("xi", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
