import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen
from supriya.typing import UGenInputMap


class BrownNoise(UGen):
    """
    A brown noise unit generator.

    ::

        >>> supriya.ugens.BrownNoise.ar()
        BrownNoise.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
