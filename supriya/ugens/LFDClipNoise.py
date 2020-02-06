import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class LFDClipNoise(UGen):
    """
    A clipped noise generator.

    ::

        >>> supriya.ugens.LFDClipNoise.ar()
        LFDClipNoise.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
