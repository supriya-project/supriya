import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen


class LFPulse(PureUGen):
    """
    A non-band-limited pulse oscillator.

    ::

        >>> supriya.ugens.LFPulse.ar()
        LFPulse.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Oscillator UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0), ("width", 0.5)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
