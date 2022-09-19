from .bases import UGen, param, ugen


@ugen(ar=True, is_multichannel=True)
class GrainBuf(UGen):
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

    trigger = param(0)
    duration = param(1)
    buffer_id = param(None)
    rate = param(1)
    position = param(0)
    interpolate = param(2)
    pan = param(0)
    envelope_buffer_id = param(-1)
    maximum_overlap = param(512)


@ugen(ar=True, is_multichannel=True)
class GrainIn(UGen):
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

    trigger = param(0)
    duration = param(1)
    source = param(None)
    position = param(0)
    envelope_buffer_id = param(-1)
    maximum_overlap = param(512)


@ugen(ar=True)
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

    source = param(None)
    window_size = param(0.2)
    pitch_ratio = param(1.0)
    pitch_dispersion = param(0.0)
    time_dispersion = param(0.0)


@ugen(ar=True, is_multichannel=True)
class Warp1(UGen):
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
        Warp1.ar()

    """

    buffer_id = param(0)
    pointer = param(0)
    frequency_scaling = param(1)
    window_size = param(0.2)
    envelope_buffer_id = param(-1)
    overlaps = param(8)
    window_rand_ratio = param(0)
    interpolation = param(1)
