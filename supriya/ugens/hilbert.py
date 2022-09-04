from .bases import UGen
from .decorators import param, ugen


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
        FreqShift.ar()

    """

    source = param(None)
    frequency = param(0.0)
    phase = param(0.0)


@ugen(ar=True, is_multichannel=True, fixed_channel_count=2)
class Hilbert(UGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert = supriya.ugens.Hilbert.ar(
        ...     source=source,
        ... )
        >>> hilbert
        UGenArray({2})

    """

    source = param(None)


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
        HilbertFIR.ar()

    """

    source = param(None)
    buffer_id = param(None)
