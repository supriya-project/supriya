import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class HenonC(UGen):
    """
    A cubic-interpolating henon map chaotic generator.

    ::

        >>> henon_c = supriya.ugens.HenonC.ar(
        ...     a=1.4,
        ...     b=0.3,
        ...     frequency=22050,
        ...     x_0=0,
        ...     x_1=0,
        ...     )
        >>> henon_c
        HenonC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    _ordered_input_names = collections.OrderedDict(
        [('frequency', 22050), ('a', 1.4), ('b', 0.3), ('x_0', 0), ('x_1', 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
