import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LFDNoise0(UGen):
    """
    A dynamic step noise generator.

    ::

        >>> supriya.ugens.LFDNoise0.ar()
        LFDNoise0.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    _ordered_input_names = collections.OrderedDict([('frequency', 500.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
