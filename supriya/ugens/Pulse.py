import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Pulse(UGen):
    """
    Band limited pulse wave generator with pulse width modulation.

    ::

        >>> pulse = supriya.ugens.Pulse.ar(
        ...     frequency=440,
        ...     width=0.5,
        ...     )
        >>> pulse
        Pulse.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict([("frequency", 440), ("width", 0.5)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
