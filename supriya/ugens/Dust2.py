import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Dust2(UGen):
    """
    A bipolar random impulse generator.

    ::

        >>> dust_2 = supriya.ugens.Dust2.ar(
        ...    density=23,
        ...    )
        >>> dust_2
        Dust2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("density", 0.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
