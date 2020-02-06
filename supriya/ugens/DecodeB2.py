import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class DecodeB2(MultiOutUGen):
    """
    A 2D Ambisonic B-format decoder.

    ::

        >>> source = supriya.ugens.PinkNoise.ar()
        >>> w, x, y = supriya.ugens.PanB2.ar(
        ...     source=source,
        ...     azimuth=supriya.ugens.SinOsc.kr(),
        ...     )
        >>> channel_count = 4
        >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
        ...     channel_count=channel_count,
        ...     orientation=0.5,
        ...     w=w,
        ...     x=x,
        ...     y=y,
        ...     )
        >>> decode_b_2
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Ambisonics UGens"

    _default_channel_count = 4

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict(
        [("w", None), ("x", None), ("y", None), ("orientation", 0.5)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
