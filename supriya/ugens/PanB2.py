import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class PanB2(MultiOutUGen):
    """
    A 2D ambisonic b-format panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_b_2 = supriya.ugens.PanB2.ar(
        ...     azimuth=0,
        ...     gain=1,
        ...     source=source,
        ...     )
        >>> pan_b_2
        UGenArray({3})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Spatialization UGens"

    _default_channel_count = 3

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("azimuth", 0), ("gain", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
