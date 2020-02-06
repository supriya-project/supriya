import collections

from supriya import CalculationRate, SignalRange
from supriya.synthdefs import UGen


class Dust(UGen):
    """
    A unipolar random impulse generator.

    ::

        >>> dust = supriya.ugens.Dust.ar(
        ...    density=23,
        ...    )
        >>> dust
        Dust.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("density", 0.0)])

    _signal_range = SignalRange.UNIPOLAR

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
