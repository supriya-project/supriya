import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class Balance2(MultiOutUGen):
    """
    A stereo signal balancer.

    ::

        >>> left = supriya.ugens.WhiteNoise.ar()
        >>> right = supriya.ugens.SinOsc.ar()
        >>> balance_2 = supriya.ugens.Balance2.ar(
        ...     left=left,
        ...     level=1,
        ...     position=0,
        ...     right=right,
        ...     )
        >>> balance_2
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Spatialization UGens"

    _default_channel_count = 2

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [("left", None), ("right", None), ("position", 0.0), ("level", 1.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
