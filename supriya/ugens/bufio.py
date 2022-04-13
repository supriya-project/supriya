import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen, WidthFirstUGen


class BufRd(MultiOutUGen):
    """
    A buffer-reading oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
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

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("phase", 0.0), ("loop", 1.0), ("interpolation", 2.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BufWr(UGen):
    """
    A buffer-writing oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
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

    _has_done_flag = True
    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("phase", 0.0), ("loop", 1.0), ("source", None)]
    )
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class ClearBuf(WidthFirstUGen):
    """

    ::

        >>> clear_buf = supriya.ugens.ClearBuf.ir(
        ...     buffer_id=23,
        ... )
        >>> clear_buf
        ClearBuf.ir()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class LocalBuf(WidthFirstUGen):
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
        ...     pv_chain = supriya.ugens.FFT(
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

    _ordered_input_names = collections.OrderedDict(
        [("channel_count", 1), ("frame_count", 1)]
    )
    _valid_calculation_rates = (CalculationRate.SCALAR,)

    ### INITIALIZER ###

    def __init__(self, frame_count=1, channel_count=1, calculation_rate=None):
        import supriya.synthdefs

        if calculation_rate is None:
            calculation_rate = supriya.CalculationRate.SCALAR
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            frame_count=frame_count,
        )


class MaxLocalBufs(UGen):
    """
    Sets the maximum number of local buffers in a synth.

    Used internally by LocalBuf.

    ::

        >>> max_local_bufs = supriya.ugens.MaxLocalBufs(1)
        >>> max_local_bufs
        MaxLocalBufs.ir()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("maximum", 0)])
    _valid_calculation_rates = (CalculationRate.SCALAR,)

    ### INITIALIZER ###

    def __init__(self, maximum=0):
        import supriya.synthdefs

        maximum = float(maximum)
        calculation_rate = supriya.CalculationRate.SCALAR
        UGen.__init__(self, calculation_rate=calculation_rate, maximum=maximum)

    ### PUBLIC METHODS ###

    def increment(self):
        """
        Increments maximum local buffer count.

        ::

            >>> max_local_bufs = supriya.ugens.MaxLocalBufs(1)
            >>> max_local_bufs.maximum
            1.0

        ::

            >>> max_local_bufs.increment()
            >>> max_local_bufs.maximum
            2.0

        Returns none.
        """
        self._inputs[0] += 1


class PlayBuf(MultiOutUGen):
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

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("rate", 1),
            ("trigger", 1),
            ("start_position", 0),
            ("loop", 0),
            ("done_action", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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

    _has_done_flag = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("offset", 0),
            ("record_level", 1),
            ("preexisting_level", 0),
            ("run", 1),
            ("loop", 1),
            ("trigger", 1),
            ("done_action", 0),
            ("source", None),
        ]
    )
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
