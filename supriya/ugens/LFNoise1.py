import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class LFNoise1(UGen):
    """
    A ramp noise generator.

    ::

        >>> supriya.ugens.LFNoise1.ar()
        LFNoise1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
