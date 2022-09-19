from .. import CalculationRate, DoneAction
from .bases import UGen, param, ugen


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
        UGenArray({2})

    """

    buffer_id = param(None)
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
        BufWr.ar()

    """

    buffer_id = param(None)
    phase = param(0.0)
    loop = param(1.0)
    source = param(None, unexpanded=True)


@ugen(ir=True, is_width_first=True)
class ClearBuf(UGen):
    """

    ::

        >>> clear_buf = supriya.ugens.ClearBuf.ir(
        ...     buffer_id=23,
        ... )
        >>> clear_buf
        ClearBuf.ir()

    """

    buffer_id = param(None)


@ugen(ir=True, is_width_first=True)
class LocalBuf(UGen):
    """
    A synth-local buffer.

    ::

        >>> local_buf = supriya.ugens.LocalBuf(
        ...     channel_count=1,
        ...     frame_count=1,
        ... )
        >>> local_buf
        LocalBuf.ir()

    LocalBuf creates a ``MaxLocalBufs`` UGen implicitly during SynthDef
    compilation:

    ::

        >>> with supriya.synthdefs.SynthDefBuilder() as builder:
        ...     local_buf = supriya.ugens.LocalBuf(2048)
        ...     source = supriya.ugens.PinkNoise.ar()
        ...     pv_chain = supriya.ugens.FFT.kr(
        ...         buffer_id=local_buf,
        ...         source=source,
        ...     )
        ...     ifft = supriya.ugens.IFFT.ar(pv_chain=pv_chain)
        ...     out = supriya.ugens.Out.ar(bus=0, source=ifft)
        ...
        >>> synthdef = builder.build()
        >>> for ugen in synthdef.ugens:
        ...     ugen
        ...
        MaxLocalBufs.ir()
        LocalBuf.ir()
        PinkNoise.ar()
        FFT.kr()
        IFFT.ar()
        Out.ar()

    """

    ### CLASS VARIABLES ###

    channel_count = param(1)
    frame_count = param(1)

    ### INITIALIZER ###

    def __init__(self, frame_count=1, channel_count=1, calculation_rate=None):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.SCALAR,
            channel_count=channel_count,
            frame_count=frame_count,
        )


@ugen(ir=True)
class MaxLocalBufs(UGen):
    """
    Sets the maximum number of local buffers in a synth.

    Used internally by LocalBuf.

    ::

        >>> max_local_bufs = supriya.ugens.MaxLocalBufs.ir(maximum=1)
        >>> max_local_bufs
        MaxLocalBufs.ir()

    """

    maximum = param(0)

    def increment(self):
        """
        Increments maximum local buffer count.

        ::

            >>> max_local_bufs = supriya.ugens.MaxLocalBufs.ir(maximum=1)
            >>> max_local_bufs.inputs
            (1.0,)

        ::

            >>> max_local_bufs.increment()
            >>> max_local_bufs.inputs
            (2.0,)

        Returns none.
        """
        self._inputs[0] += 1


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
        UGenArray({2})

    """

    buffer_id = param(None)
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
        RecordBuf.ar()

    """

    buffer_id = param(None)
    offset = param(0.0)
    record_level = param(1.0)
    preexisting_level = param(0.0)
    run = param(1.0)
    loop = param(1.0)
    trigger = param(1.0)
    done_action = param(DoneAction(0))
    source = param(None, unexpanded=True)
