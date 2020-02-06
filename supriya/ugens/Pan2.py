import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class Pan2(MultiOutUGen):
    """
    A two channel equal power panner.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> pan_2 = supriya.ugens.Pan2.ar(
        ...     source=source,
        ...     )
        >>> pan_2
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Spatialization UGens"

    _default_channel_count = 2

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("position", 0.0), ("level", 1.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
