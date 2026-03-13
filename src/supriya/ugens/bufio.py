from typing import Any

from ..enums import CalculationRate, DoneAction
from ..typing import DEFAULT, Default
from .core import UGen, param, ugen


@ugen(ar=True, kr=True, is_multichannel=True)
class BufRd(UGen):
    """
    A buffer-reading oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id=buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id=buffer_id),
        ... )
        >>> buf_rd = supriya.ugens.BufRd.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     interpolation=2,
        ...     loop=1,
        ...     phase=phase,
        ... )
        >>> buf_rd
        <BufRd.ar()>
    """

    buffer_id = param()
    phase = param(0.0)
    loop = param(1)
    interpolation = param(2)


@ugen(ar=True, kr=True, has_done_flag=True)
class BufWr(UGen):
    """
    A buffer-writing oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id=buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id=buffer_id),
        ... )
        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> buf_wr = supriya.ugens.BufWr.ar(
        ...     buffer_id=buffer_id,
        ...     loop=1,
        ...     phase=phase,
        ...     source=source,
        ... )
        >>> buf_wr
        <BufWr.ar()[0]>
    """

    buffer_id = param()
    phase = param(0.0)
    loop = param(1.0)
    source = param(unexpanded=True)


@ugen(ir=True, is_width_first=True)
class ClearBuf(UGen):
    """
    ::

        >>> clear_buf = supriya.ugens.ClearBuf.ir(
        ...     buffer_id=23,
        ... )
        >>> clear_buf
        <ClearBuf.ir()[0]>
    """

    buffer_id = param()


@ugen(ir=True, is_width_first=True)
class LocalBuf(UGen):
    """
    A synth-local buffer.

    ::

        >>> from supriya.ugens import FFT, IFFT, LocalBuf, Out, PinkNoise, SynthDefBuilder

    ::

        >>> local_buf = LocalBuf.ir(
        ...     channel_count=1,
        ...     frame_count=1,
        ... )
        >>> local_buf
        <LocalBuf.ir()[0]>

    LocalBuf creates a ``MaxLocalBufs`` UGen implicitly during SynthDef compilation:

    ::

        >>> with SynthDefBuilder() as builder:
        ...     local_buf = LocalBuf.ir(frame_count=2048)
        ...     source = PinkNoise.ar()
        ...     pv_chain = FFT.kr(
        ...         buffer_id=local_buf,
        ...         source=source,
        ...     )
        ...     ifft = IFFT.ar(pv_chain=pv_chain)
        ...     out = Out.ar(bus=0, source=ifft)
        ...
        >>> synthdef = builder.build()
        >>> for ugen in synthdef.ugens:
        ...     ugen
        ...
        <MaxLocalBufs.ir()>
        <LocalBuf.ir()>
        <PinkNoise.ar()>
        <FFT.kr()>
        <IFFT.ar()>
        <Out.ar()>
    """

    channel_count = param(1)
    frame_count = param(1)

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        return CalculationRate.SCALAR, kwargs


@ugen(ir=True)
class MaxLocalBufs(UGen):
    """
    Sets the maximum number of local buffers in a synth.

    Used internally by LocalBuf.

    ::

        >>> max_local_bufs = supriya.ugens.MaxLocalBufs.ir(maximum=1)
        >>> max_local_bufs
        <MaxLocalBufs.ir()[0]>
    """

    maximum = param(0)


@ugen(ar=True, kr=True, is_multichannel=True)
class PlayBuf(UGen):
    """
    A sample playback oscillator.

    ::

        >>> buffer_id = 23
        >>> play_buf = supriya.ugens.PlayBuf.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     done_action=0,
        ...     loop=0,
        ...     rate=1,
        ...     start_position=0,
        ...     trigger=1,
        ... )
        >>> play_buf
        <PlayBuf.ar()>
    """

    buffer_id = param()
    rate = param(1)
    trigger = param(1)
    start_position = param(0)
    loop = param(0)
    done_action = param(0)


@ugen(ar=True, kr=True, has_done_flag=True)
class RecordBuf(UGen):
    """
    Records or overdubs into a buffer.

    ::

        >>> buffer_id = 23
        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> record_buf = supriya.ugens.RecordBuf.ar(
        ...     buffer_id=buffer_id,
        ...     done_action=0,
        ...     loop=1,
        ...     offset=0,
        ...     preexisting_level=0,
        ...     record_level=1,
        ...     run=1,
        ...     source=source,
        ...     trigger=1,
        ... )
        >>> record_buf
        <RecordBuf.ar()[0]>
    """

    buffer_id = param()
    offset = param(0.0)
    record_level = param(1.0)
    preexisting_level = param(0.0)
    run = param(1.0)
    loop = param(1.0)
    trigger = param(1.0)
    done_action = param(DoneAction(0))
    source = param(unexpanded=True)


@ugen(ar=True, kr=True)
class ScopeOut(UGen):
    """
    Utility UGen for scope output on remote servers.

    ::

        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> scope_out = supriya.ugens.ScopeOut.ar(
        ...     source=source,
        ...     buffer_id=0,
        ... )
        >>> scope_out
        <ScopeOut.ar()[0]>

    """

    buffer_id = param()
    source = param(unexpanded=True)


@ugen(ar=True, kr=True)
class ScopeOut2(UGen):
    """
    Utility UGen for scope output on local servers.

    ::

        >>> source = supriya.ugens.In.ar(bus=0, channel_count=2)
        >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
        ...     source=source,
        ...     scope_id=0,
        ...     max_frames=8192,
        ...     scope_frames=2048,
        ... )
        >>> scope_out_2
        <ScopeOut2.ar()[0]>

    """

    scope_id = param()
    max_frames = param(4096)
    scope_frames = param(DEFAULT)
    source = param(unexpanded=True)

    def _postprocess_kwargs(
        self, *, calculation_rate: CalculationRate, **kwargs
    ) -> tuple[CalculationRate, dict[str, Any]]:
        if isinstance(kwargs["scope_frames"], Default):
            kwargs["scope_frames"] = kwargs["max_frames"]
        return calculation_rate, kwargs
