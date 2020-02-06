import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen
from supriya.typing import UGenInputMap


class PinkNoise(UGen):
    """
    A pink noise unit generator.

    ::

        >>> supriya.ugens.PinkNoise.ar()
        PinkNoise.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
