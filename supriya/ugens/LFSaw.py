import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class LFSaw(PureUGen):
    """
    A non-band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.LFSaw.ar()
        LFSaw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Oscillator UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
