import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen


class GrainBuf(MultiOutUGen):
    """

    ::

        >>> grain_buf = supriya.ugens.GrainBuf.ar(
        ...     channel_count=2,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     interpolate=2,
        ...     maximum_overlap=512,
        ...     pan=0,
        ...     position=0,
        ...     rate=1,
        ...     buffer_id=0,
        ...     trigger=0,
        ... )
        >>> grain_buf
        UGenArray({2})

    """

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("trigger", 0),
            ("duration", 1),
            ("buffer_id", None),
            ("rate", 1),
            ("position", 0),
            ("interpolate", 2),
            ("pan", 0),
            ("envelope_buffer_id", -1),
            ("maximum_overlap", 512),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class GrainIn(MultiOutUGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> grain_in = supriya.ugens.GrainIn.ar(
        ...     channel_count=2,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     maximum_overlap=512,
        ...     position=0,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> grain_in
        UGenArray({2})

    """

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("trigger", 0),
            ("duration", 1),
            ("source", None),
            ("position", 0),
            ("envelope_buffer_id", -1),
            ("maximum_overlap", 512),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class PitchShift(UGen):
    """
    A pitch shift unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.PitchShift.ar(
        ...     source=source,
        ... )
        PitchShift.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("window_size", 0.2),
            ("pitch_ratio", 1.0),
            ("pitch_dispersion", 0.0),
            ("time_dispersion", 0.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Warp1(MultiOutUGen):
    """

    ::

        >>> warp_1 = supriya.ugens.Warp1.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     envelope_buffer_id=-1,
        ...     frequency_scaling=1,
        ...     interpolation=1,
        ...     overlaps=8,
        ...     pointer=0,
        ...     window_rand_ratio=0,
        ...     window_size=0.2,
        ... )
        >>> warp_1
        Warp1.ar()[0]

    """

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", 0),
            ("pointer", 0),
            ("frequency_scaling", 1),
            ("window_size", 0.2),
            ("envelope_buffer_id", -1),
            ("overlaps", 8),
            ("window_rand_ratio", 0),
            ("interpolation", 1),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)
