import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class BiPanB2(MultiOutUGen):
    """
    A 2D ambisonic b-format panner.

    ::

        >>> in_a = supriya.ugens.SinOsc.ar()
        >>> in_b = supriya.ugens.WhiteNoise.ar()
        >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
        ...     azimuth=-0.5,
        ...     gain=1,
        ...     in_a=in_a,
        ...     in_b=in_b,
        ...     )
        >>> bi_pan_b_2
        UGenArray({3})

    ::

        >>> w, x, y = bi_pan_b_2

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    _default_channel_count = 3

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [('in_a', None), ('in_b', None), ('azimuth', None), ('gain', 1.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
