import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Blip(UGen):
    """
    A band limited impulse generator.

    ::

        >>> blip = supriya.ugens.Blip.ar(
        ...     frequency=440,
        ...     harmonic_count=200,
        ...     )
        >>> blip
        Blip.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Oscillator UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("harmonic_count", 200.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
