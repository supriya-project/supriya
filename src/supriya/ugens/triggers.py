from ..enums import CalculationRate
from .core import OutputProxy, UGen, param, ugen


@ugen(ar=True, kr=True, ir=True)
class Clip(UGen):
    """
    Clips a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> clip = supriya.ugens.Clip.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> clip
        <Clip.ar()[0]>
    """

    source = param()
    minimum = param(0.0)
    maximum = param(1.0)


@ugen(ar=True, kr=True, ir=True)
class Fold(UGen):
    """
    Folds a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> fold = supriya.ugens.Fold.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> fold
        <Fold.ar()[0]>
    """

    source = param()
    minimum = param(0.0)
    maximum = param(1.0)


@ugen(ar=True, kr=True)
class Gate(UGen):
    """
    Gates or holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(density=1)
        >>> gate = supriya.ugens.Gate.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> gate
        <Gate.ar()[0]>
    """

    source = param()
    trigger = param(0)


@ugen(ar=True, kr=True, ir=True)
class InRange(UGen):
    """
    Tests if a signal is within a given range.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> in_range = supriya.ugens.InRange.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> in_range
        <InRange.ar()[0]>
    """

    source = param()
    minimum = param(0.0)
    maximum = param(1.0)


@ugen(ar=True, kr=True)
class Latch(UGen):
    """
    Samples and holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(density=1)
        >>> latch = supriya.ugens.Latch.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> latch
        <Latch.ar()[0]>
    """

    source = param()
    trigger = param(0)


@ugen(ar=True, kr=True)
class LeastChange(UGen):
    """
    Outputs least changed input.

    ::

        >>> least_change = supriya.ugens.LeastChange.ar(
        ...     a=0,
        ...     b=0,
        ... )
        >>> least_change
        <LeastChange.ar()[0]>
    """

    a = param(0)
    b = param(0)


@ugen(ar=True, kr=True)
class MostChange(UGen):
    """
    Outputs most changed input.

    ::

        >>> most_change = supriya.ugens.MostChange.ar(
        ...     a=0,
        ...     b=0,
        ... )
        >>> most_change
        <MostChange.ar()[0]>
    """

    a = param(0)
    b = param(0)


@ugen(ar=True, kr=True)
class Peak(UGen):
    """
    Tracks peak signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> peak = supriya.ugens.Peak.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> peak
        <Peak.ar()[0]>
    """

    source = param()
    trigger = param(0)


@ugen(ar=True, kr=True)
class PeakFollower(UGen):
    """
    Tracks peak signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> peak_follower = supriya.ugens.PeakFollower.ar(
        ...     decay=0.999,
        ...     source=source,
        ... )
        >>> peak_follower
        <PeakFollower.ar()[0]>
    """

    source = param()
    decay = param(0.999)


@ugen(ar=True, kr=True)
class Phasor(UGen):
    """
    A resettable linear ramp between two levels.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=0.5)
        >>> phasor = supriya.ugens.Phasor.ar(
        ...     rate=1,
        ...     reset_pos=0,
        ...     start=0,
        ...     stop=1,
        ...     trigger=trigger,
        ... )
        >>> phasor
        <Phasor.ar()[0]>
    """

    trigger = param(0)
    rate = param(1.0)
    start = param(0.0)
    stop = param(1.0)
    reset_pos = param(0.0)


@ugen(ar=True, kr=True)
class Poll(UGen):
    """
    A UGen poller.

    ::

        >>> sine = supriya.ugens.SinOsc.ar()
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> poll = supriya.ugens.Poll.ar(
        ...     source=sine,
        ...     trigger=trigger,
        ...     trigger_id=1234,
        ... )
        >>> poll
        <Poll.ar()[0]>

    .. container:: example

        Unlike **sclang**, Python does not share any inter-process communication with
        **scsynth**. This means that the Poll UGen is not able to automatically print
        out its diagnostic messages into a Python interpreter session.

        To get information out of the Poll UGen, we first need to set the Poll's
        `trigger_id` to a value greater than 0. This will cause the poll to send `/tr`
        OSC messages back to its client - Python. We can then register a callback to
        respond to these `/tr` messages.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     sine = supriya.ugens.SinOsc.ar()
            ...     trigger = supriya.ugens.Impulse.kr(frequency=1)
            ...     poll = supriya.ugens.Poll.ar(
            ...         source=sine,
            ...         trigger=trigger,
            ...         trigger_id=1234,
            ...     )
            ...
            >>> synthdef = builder.build()

        ::

            >>> server = supriya.Server().boot(port=supriya.osc.find_free_port())
            >>> _ = server.add_synthdefs(
            ...     synthdef,
            ...     on_completion=lambda context: context.add_synth(synthdef),
            ... )
            >>> _ = server.sync()
            >>> callback = server.osc_protocol.register(
            ...     pattern="/tr",
            ...     procedure=lambda message: print(
            ...         "Polled: {!r}".format(message)
            ...     ),
            ...     once=True,
            ... )

        ::

            >>> _ = server.quit()
    """

    ### CLASS VARIABLES ###

    trigger = param()
    source = param()
    trigger_id = param(-1)
    label = param(unexpanded=True)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        label=None,
        source=None,
        special_index=None,
        trigger=None,
        trigger_id=-1,
    ):
        if label is None:
            if isinstance(source, UGen):
                label = type(source).__name__
            elif isinstance(source, OutputProxy):
                label = type(source.ugen).__name__
        label = str(label)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            label=[len(label), *(ord(c) for c in label)],
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, label=None, source=None, trigger=None, trigger_id=-1):
        return cls._new_expanded(
            calculation_rate=CalculationRate.AUDIO,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )

    @classmethod
    def kr(cls, label=None, source=None, trigger=None, trigger_id=-1):
        return cls._new_expanded(
            calculation_rate=CalculationRate.CONTROL,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )

    @classmethod
    def new(cls, label=None, source=None, trigger=None, trigger_id=-1):
        return cls._new_expanded(
            calculation_rate=[CalculationRate.from_expr(x) for x in source],
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )


@ugen(ar=True, kr=True)
class RunningMax(UGen):
    """
    Tracks maximum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> running_max = supriya.ugens.RunningMax.ar(
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> running_max
        <RunningMax.ar()[0]>
    """

    source = param()
    trigger = param(0)


@ugen(ar=True, kr=True)
class RunningMin(UGen):
    """
    Tracks minimum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> running_min = supriya.ugens.RunningMin.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> running_min
        <RunningMin.ar()[0]>
    """

    source = param()
    trigger = param(0)


@ugen(ar=True, kr=True)
class Schmidt(UGen):
    """
    A Schmidt trigger.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> schmidt = supriya.ugens.Schmidt.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> schmidt
        <Schmidt.ar()[0]>
    """

    source = param()
    minimum = param(0.0)
    maximum = param(1.0)


@ugen(ar=True, kr=True, channel_count=0, fixed_channel_count=True)
class SendPeakRMS(UGen):
    """
    Tracks peak and power of a signal for GUI applications.

    ::

        >>> send_peak_rms = supriya.ugens.SendPeakRMS.kr(
        ...     command_name="/reply",
        ...     peak_lag=3,
        ...     reply_id=-1,
        ...     reply_rate=20,
        ...     source=[1, 2, 3],
        ... )
        >>> send_peak_rms
        <SendPeakRMS.kr()>
    """

    ### CLASS VARIABLES ###

    reply_rate = param(20)
    peak_lag = param(3)
    reply_id = param(-1)
    source_size = param()
    source = param(unexpanded=True)
    character_count = param()
    character = param(unexpanded=True)

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls, command_name="/reply", peak_lag=3, reply_id=-1, reply_rate=20, source=None
    ):
        """
        Constructs an audio-rate SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.ar(
            ...     command_name="/reply",
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ... )
            >>> send_peak_rms
            <SendPeakRMS.ar()>

        Returns ugen graph.
        """
        command = str(command_name)
        return cls._new_single(
            calculation_rate=CalculationRate.AUDIO,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            source=source,
            source_size=len(source),
            character_count=len(command),
            character=[ord(x) for x in command],
        )

    @classmethod
    def kr(
        cls, command_name="/reply", peak_lag=3, reply_id=-1, reply_rate=20, source=None
    ):
        """
        Constructs a control-rate SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.kr(
            ...     command_name="/reply",
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ... )
            >>> send_peak_rms
            <SendPeakRMS.kr()>

        Returns ugen graph.
        """
        command = str(command_name)
        return cls._new_single(
            calculation_rate=CalculationRate.CONTROL,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            source=source,
            source_size=len(source),
            character_count=len(command),
            character=[ord(x) for x in command],
        )


@ugen(ar=True, kr=True, channel_count=0, fixed_channel_count=True)
class SendReply(UGen):
    """
    Sends an array of values from the server to all notified clients.

    ::

        >>> source = supriya.ugens.In.ar(channel_count=4)
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
        >>> send_reply = supriya.ugens.SendReply.kr(
        ...     command_name="/reply",
        ...     source=source,
        ...     trigger=trigger,
        ... )
    """

    trigger = param()
    reply_id = param(-1)
    character_count = param()
    character = param(unexpanded=True)
    source = param(unexpanded=True)

    @classmethod
    def ar(cls, command_name="/reply", reply_id=-1, source=None, trigger=None):
        """
        Constructs an audio-rate SendReply.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
            >>> send_reply = supriya.ugens.SendReply.ar(
            ...     command_name="/reply",
            ...     source=source,
            ...     trigger=trigger,
            ... )
            >>> send_reply
            <SendReply.ar()>

        Returns ugen graph.
        """
        command = str(command_name)
        return cls._new_single(
            calculation_rate=CalculationRate.AUDIO,
            trigger=trigger,
            reply_id=reply_id,
            character_count=len(command),
            character=[ord(x) for x in command],
            source=source,
        )

    @classmethod
    def kr(cls, command_name="/reply", reply_id=-1, source=None, trigger=None):
        """
        Constructs a control-rate SendReply.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> trigger = supriya.ugens.Impulse.kr(frequency=1)
            >>> send_reply = supriya.ugens.SendReply.kr(
            ...     command_name="/reply",
            ...     source=source,
            ...     trigger=trigger,
            ... )
            >>> send_reply
            <SendReply.kr()>

        Returns ugen graph.
        """
        command = str(command_name)
        return cls._new_single(
            calculation_rate=CalculationRate.CONTROL,
            trigger=trigger,
            reply_id=reply_id,
            character_count=len(command),
            character=[ord(x) for x in command],
            source=source,
        )


@ugen(ar=True, kr=True)
class SendTrig(UGen):
    trigger = param()
    id_ = param(0)
    value = param(0.0)


@ugen(ar=True, kr=True)
class Sweep(UGen):
    """
    A triggered linear ramp.

    ::

        >>> sweep = supriya.ugens.Sweep.ar(
        ...     rate=1,
        ...     trigger=0,
        ... )
        >>> sweep
        <Sweep.ar()[0]>
    """

    trigger = param(0)
    rate = param(1.0)


@ugen(ar=True, kr=True)
class TDelay(UGen):
    """
    A trigger delay.

    ::

        >>> source = supriya.ugens.Dust.kr(density=1)
        >>> tdelay = supriya.ugens.TDelay.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> tdelay
        <TDelay.ar()[0]>
    """

    source = param()
    duration = param(0.1)


@ugen(ar=True, kr=True)
class ToggleFF(UGen):
    """
    A toggle flip-flop.

    ::

        >>> trigger = supriya.ugens.Dust.kr(density=1)
        >>> toggle_ff = supriya.ugens.ToggleFF.ar(
        ...     trigger=trigger,
        ... )
        >>> toggle_ff
        <ToggleFF.ar()[0]>
    """

    trigger = param(0)


@ugen(ar=True, kr=True)
class Trig1(UGen):
    """
    A timed trigger.

    ::

        >>> source = supriya.ugens.Dust.kr(density=1)
        >>> trig_1 = supriya.ugens.Trig1.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> trig_1
        <Trig1.ar()[0]>
    """

    source = param()
    duration = param(0.1)


@ugen(ar=True, kr=True)
class Trig(UGen):
    """
    A timed trigger.

    ::

        >>> source = supriya.ugens.Dust.kr(density=1)
        >>> trig = supriya.ugens.Trig.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> trig
        <Trig.ar()[0]>
    """

    source = param()
    duration = param(0.1)


@ugen(ar=True, kr=True, ir=True)
class Wrap(UGen):
    """
    Wraps a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> wrap = supriya.ugens.Wrap.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ... )
        >>> wrap
        <Wrap.ar()[0]>
    """

    source = param()
    minimum = param(0.0)
    maximum = param(1.0)


@ugen(ar=True, kr=True)
class ZeroCrossing(UGen):
    """
    A zero-crossing frequency follower.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
        ...     source=source,
        ... )
        >>> zero_crossing
        <ZeroCrossing.ar()[0]>
    """

    source = param()
