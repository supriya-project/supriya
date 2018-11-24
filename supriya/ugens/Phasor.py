import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Phasor(UGen):
    """
    A resettable linear ramp between two levels.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(0.5)
        >>> phasor = supriya.ugens.Phasor.ar(
        ...     rate=1,
        ...     reset_pos=0,
        ...     start=0,
        ...     stop=1,
        ...     trigger=trigger,
        ...     )
        >>> phasor
        Phasor.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Trigger Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [("trigger", 0), ("rate", 1), ("start", 0), ("stop", 1), ("reset_pos", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
