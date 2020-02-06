import collections

from supriya import CalculationRate
from supriya.typing import UGenInputMap
from supriya.synthdefs import UGen


class WhiteNoise(UGen):
    """
    A white noise unit generator.

    ::

        >>> supriya.ugens.WhiteNoise.ar()
        WhiteNoise.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
