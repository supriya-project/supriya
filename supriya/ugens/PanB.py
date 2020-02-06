import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class PanB(MultiOutUGen):
    """
    A 3D ambisonic b-format panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_b = supriya.ugens.PanB.ar(
        ...     azimuth=0,
        ...     elevation=0,
        ...     gain=1,
        ...     source=source,
        ...     )
        >>> pan_b
        UGenArray({3})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Spatialization UGens"

    _default_channel_count = 3

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("azimuth", 0), ("elevation", 0), ("gain", 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
