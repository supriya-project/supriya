from .core import UGen, param, ugen


@ugen(ar=True)
class FreqShift(UGen):
    """
    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> freq_shift = supriya.ugens.FreqShift.ar(
        ...     frequency=0,
        ...     phase=0,
        ...     source=source,
        ... )
        >>> freq_shift
        <FreqShift.ar()[0]>
    """

    source = param()
    frequency = param(0.0)
    phase = param(0.0)


@ugen(ar=True, channel_count=2, fixed_channel_count=True)
class Hilbert(UGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert = supriya.ugens.Hilbert.ar(
        ...     source=source,
        ... )
        >>> hilbert
        <Hilbert.ar()>
    """

    source = param()


@ugen(ar=True)
class HilbertFIR(UGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert_fir = supriya.ugens.HilbertFIR.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> hilbert_fir
        <HilbertFIR.ar()[0]>
    """

    source = param()
    buffer_id = param()
