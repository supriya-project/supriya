import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Amplitude(UGen):
    """
    An amplitude follower.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> amplitude = supriya.ugens.Amplitude.kr(
        ...     attack_time=0.01,
        ...     release_time=0.01,
        ...     source=source,
        ...     )
        >>> amplitude
        Amplitude.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Dynamics UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("attack_time", 0.01), ("release_time", 0.01)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
