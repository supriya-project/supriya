import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LFNoise2(UGen):
    """
    A quadratic noise generator.

    ::

        >>> supriya.ugens.LFNoise2.ar()
        LFNoise2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
