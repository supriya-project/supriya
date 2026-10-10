from .core import (
    PseudoUGen,
    UGen,
    UGenOperable,
    UGenRecursiveInput,
    UGenVector,
    param,
    ugen,
)
from .delay import DelayN
from .info import BufDur
from .pv import FFT, IFFT, PV_PhaseShift90


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


class HilbertFIR(PseudoUGen):
    """
    Applies the Hilbert transform.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert_fir = supriya.ugens.HilbertFIR.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> hilbert_fir
        <UGenVector([<DelayN.ar()[0]>, <IFFT.ar()[0]>])>
    """

    source = param()
    buffer_id = param()

    @classmethod
    def ar(
        cls, *, source: UGenRecursiveInput, buffer_id: UGenRecursiveInput
    ) -> UGenOperable:
        chain = PV_PhaseShift90.kr(pv_chain=FFT.kr(buffer_id=buffer_id, source=source))
        delay_time = BufDur.kr(buffer_id=buffer_id)  # type: ignore[attr-defined]
        return UGenVector(
            DelayN.ar(
                source=source, maximum_delay_time=delay_time, delay_time=delay_time
            ),
            IFFT.ar(pv_chain=chain),
        )
