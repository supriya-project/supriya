from .bases import UGen, param, ugen


@ugen(ar=True, is_pure=True)
class BAllPass(UGen):
    """
    An all-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ball_pass = supriya.ugens.BAllPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> ball_pass
        BAllPass.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    reciprocal_of_q = param(1.0)


@ugen(ar=True, is_pure=True)
class BBandPass(UGen):
    """
    A band-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bband_pass = supriya.ugens.BBandPass.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ... )
        >>> bband_pass
        BBandPass.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    bandwidth = param(1.0)


@ugen(ar=True, is_pure=True)
class BBandStop(UGen):
    """
    A band-stop filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bband_stop = supriya.ugens.BBandStop.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ... )
        >>> bband_stop
        BBandStop.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    bandwidth = param(1.0)


@ugen(ar=True, is_pure=True)
class BHiCut(UGen):
    """
    A high-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bhi_cut = supriya.ugens.BHiCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ... )
        >>> bhi_cut
        BHiCut.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    order = param(2.0)
    max_order = param(5.0)


@ugen(ar=True, is_pure=True)
class BHiPass(UGen):
    """
    A high-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bhi_pass = supriya.ugens.BHiPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> bhi_pass
        BHiPass.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    reciprocal_of_q = param(1.0)


@ugen(ar=True, is_pure=True)
class BHiShelf(UGen):
    """
    A high-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
        ...     gain=0,
        ...     frequency=1200,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ... )
        >>> bhi_shelf
        BHiShelf.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    reciprocal_of_s = param(1.0)
    gain = param(0.0)


@ugen(ar=True, is_pure=True)
class BLowCut(UGen):
    """
    A low-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> blow_cut = supriya.ugens.BLowCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ... )
        >>> blow_cut
        BLowCut.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    order = param(2.0)
    max_order = param(5.0)


@ugen(ar=True, is_pure=True)
class BLowPass(UGen):
    """
    A low-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> blow_pass = supriya.ugens.BLowPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> blow_pass
        BLowPass.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    reciprocal_of_q = param(1.0)


@ugen(ar=True, is_pure=True)
class BLowShelf(UGen):
    """
    A low-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> blow_shelf = supriya.ugens.BLowShelf.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ... )
        >>> blow_shelf
        BLowShelf.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    reciprocal_of_s = param(1.0)
    gain = param(0.0)


@ugen(ar=True, is_pure=True)
class BPeakEQ(UGen):
    """
    A parametric equalizer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bpeak_eq = supriya.ugens.BPeakEQ.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> bpeak_eq
        BPeakEQ.ar()

    """

    source = param(None)
    frequency = param(1200.0)
    reciprocal_of_q = param(1.0)
    gain = param(0.0)
