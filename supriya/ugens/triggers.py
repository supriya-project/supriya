import collections
from collections.abc import Sequence

from supriya import CalculationRate
from supriya.synthdefs import UGen


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
        Clip.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("minimum", 0.0), ("maximum", 1.0)]
    )
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


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
        Fold.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("minimum", 0.0), ("maximum", 1.0)]
    )
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


class Gate(UGen):
    """
    Gates or holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> gate = supriya.ugens.Gate.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> gate
        Gate.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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
        InRange.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", 0), ("minimum", 0), ("maximum", 1)]
    )
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


class Latch(UGen):
    """
    Samples and holds.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> latch = supriya.ugens.Latch.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> latch
        Latch.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LeastChange(UGen):
    """
    Outputs least changed input.

    ::

        >>> least_change = supriya.ugens.LeastChange.ar(
        ...     a=0,
        ...     b=0,
        ... )
        >>> least_change
        LeastChange.ar()

    """

    _ordered_input_names = collections.OrderedDict([("a", 0), ("b", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class MostChange(UGen):
    """
    Outputs most changed input.

    ::

        >>> most_change = supriya.ugens.MostChange.ar(
        ...     a=0,
        ...     b=0,
        ... )
        >>> most_change
        MostChange.ar()

    """

    _ordered_input_names = collections.OrderedDict([("a", 0), ("b", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Peak(UGen):
    """
    Tracks peak signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> peak = supriya.ugens.Peak.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> peak
        Peak.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class PeakFollower(UGen):
    """
    Tracks peak signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> peak_follower = supriya.ugens.PeakFollower.ar(
        ...     decay=0.999,
        ...     source=source,
        ... )
        >>> peak_follower
        PeakFollower.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("decay", 0.999)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Phasor(UGen):
    """
    A resettable linear ramp between two levels.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(0.5)
        >>> phasor = supriya.ugens.Phasor.ar(
        ...     rate=1,
        ...     reset_pos=0,
        ...     start=0,
        ...     stop=1,
        ...     trigger=trigger,
        ... )
        >>> phasor
        Phasor.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("trigger", 0), ("rate", 1), ("start", 0), ("stop", 1), ("reset_pos", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Poll(UGen):
    """
    A UGen poller.

    ::

        >>> sine = supriya.ugens.SinOsc.ar()
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> poll = supriya.ugens.Poll.ar(
        ...     source=sine,
        ...     trigger=trigger,
        ...     trigger_id=1234,
        ... )
        >>> poll
        Poll.ar()

    ..  container:: example

        Unlike **sclang**, Python does not share any inter-process
        communication with **scsynth**. This means that the Poll UGen is not
        able to automatically print out its diagnostic messages into a Python
        interpreter session.

        To get information out of the Poll UGen, we first need to set the
        Poll's `trigger_id` to a value greater than 0. This will cause the poll
        to send `/tr` OSC messages back to its client - Python. We can then
        register a callback to respond to these `/tr` messages.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     sine = supriya.ugens.SinOsc.ar()
            ...     trigger = supriya.ugens.Impulse.kr(1)
            ...     poll = supriya.ugens.Poll.ar(
            ...         source=sine,
            ...         trigger=trigger,
            ...         trigger_id=1234,
            ...     )
            ...
            >>> synthdef = builder.build()

        ::

            >>> server = supriya.Server().boot()
            >>> synth = supriya.Synth(synthdef).allocate(server)
            >>> callback = server.osc_protocol.register(
            ...     pattern="/tr",
            ...     procedure=lambda response: print(
            ...         "Poll value is: {}".format(response.value)
            ...     ),
            ...     once=True,
            ... )

        ::

            >>> server.quit()
            <Server: offline>

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("source", None), ("trigger_id", -1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        label=None,
        source=None,
        trigger=None,
        trigger_id=-1,
    ):
        import supriya.synthdefs
        import supriya.ugens

        if label is None:
            if isinstance(source, supriya.synthdefs.UGen):
                label = type(source).__name__
            elif isinstance(source, supriya.synthdefs.OutputProxy):
                label = type(source.source).__name__
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )
        label = str(label)
        self._configure_input("label", len(label))
        for character in label:
            self._configure_input("label", ord(character))

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, label=None, source=None, trigger=None, trigger_id=-1):
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )
        return ugen

    @classmethod
    def kr(cls, label=None, source=None, trigger=None, trigger_id=-1):
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )
        return ugen

    @classmethod
    def new(cls, label=None, source=None, trigger=None, trigger_id=-1):
        import supriya.synthdefs

        if isinstance(source, Sequence):
            source = (source,)
        calculation_rates = []
        for single_source in source:
            rate = supriya.CalculationRate.from_expr(single_source)
            calculation_rates.append(rate)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rates,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
        )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def label(self):
        """
        Gets `label` input of Poll.

        ::

            >>> sine = supriya.ugens.SinOsc.ar()
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> poll = supriya.ugens.Poll.ar(
            ...     label="Foo",
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ... )
            >>> poll.label
            'Foo'

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("trigger_id") + 2
        characters = self._inputs[index:]
        characters = [chr(int(_)) for _ in characters]
        label = "".join(characters)
        return label


class RunningMax(Peak):
    """
    Tracks maximum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> running_max = supriya.ugens.RunningMax.ar(
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> running_max
        RunningMax.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class RunningMin(Peak):
    """
    Tracks minimum signal amplitude.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> running_min = supriya.ugens.RunningMin.ar(
        ...     source=source,
        ...     trigger=trigger,
        ... )
        >>> running_min
        RunningMin.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("trigger", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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
        Schmidt.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", 0), ("minimum", 0), ("maximum", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class SendPeakRMS(UGen):
    """
    Tracks peak and power of a signal for GUI applications.

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
        SendPeakRMS.kr()

    """

    ### CLASS VARIABLES ###

    _default_channel_count = 0
    _ordered_input_names = collections.OrderedDict(
        [("reply_rate", 20), ("peak_lag", 3), ("reply_id", -1)]
    )
    _unexpanded_argument_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        command_name="/reply",
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        source=None,
    ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
        )
        command_name = str(command_name)
        if not isinstance(source, Sequence):
            source = (source,)
        self._configure_input("source", len(source))
        for input_ in source:
            self._configure_input("source", input_)
        self._configure_input("command_name", len(command_name))
        for character in command_name:
            self._configure_input("label", ord(character))

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
            SendPeakRMS.ar()

        Returns ugen graph.
        """
        calculation_rate = CalculationRate.AUDIO
        ugen = cls._new_single(
            calculation_rate=calculation_rate,
            command_name=command_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            source=source,
        )
        return ugen

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
            SendPeakRMS.kr()

        Returns ugen graph.
        """
        calculation_rate = CalculationRate.CONTROL
        ugen = cls._new_single(
            calculation_rate=calculation_rate,
            command_name=command_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            source=source,
        )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def command_name(self):
        """
        Gets `command_name` input of SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.ar(
            ...     command_name="/reply",
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ... )
            >>> send_peak_rms.command_name
            '/reply'

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("reply_id") + 1
        source_length = int(self._inputs[index])
        index += source_length + 2
        characters = self._inputs[index:]
        characters = [chr(int(_)) for _ in characters]
        command_name = "".join(characters)
        return command_name

    @property
    def source(self):
        """
        Gets `source` input of SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.ar(
            ...     command_name="/reply",
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ... )
            >>> send_peak_rms.source
            (In.ar()[0], In.ar()[1], In.ar()[2], In.ar()[3])

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("reply_id") + 1
        source_length = int(self._inputs[index])
        start = index + 1
        stop = start + source_length
        return tuple(self._inputs[start:stop])


class SendReply(UGen):
    """
    Sends an array of values from the server to all notified clients.

        >>> source = supriya.ugens.In.ar(channel_count=4)
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> send_peak_rms = supriya.ugens.SendReply.kr(
        ...     command_name="/reply",
        ...     source=source,
        ...     trigger=trigger,
        ... )

    """

    ### CLASS VARIABLES ###

    _default_channel_count = 0
    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("reply_id", -1)]
    )
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        command_name="/reply",
        reply_id=-1,
        trigger=None,
        source=None,
    ):
        UGen.__init__(
            self, calculation_rate=calculation_rate, reply_id=reply_id, trigger=trigger
        )
        self._configure_input("size", len(command_name))
        for i, character in enumerate(command_name):
            self._configure_input(("char", i), ord(character))
        self._configure_input("source", source)

    @classmethod
    def ar(cls, command_name="/reply", reply_id=-1, source=None, trigger=None):
        """
        Constructs an audio-rate SendReply.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> send_reply = supriya.ugens.SendReply.ar(
            ...     command_name="/reply",
            ...     source=source,
            ...     trigger=trigger,
            ... )
            >>> send_reply
            SendReply.ar()

        Returns ugen graph.
        """
        calculation_rate = CalculationRate.AUDIO
        ugen = cls._new_single(
            calculation_rate=calculation_rate,
            command_name=command_name,
            reply_id=reply_id,
            source=source,
            trigger=trigger,
        )
        return ugen

    @classmethod
    def kr(cls, command_name="/reply", reply_id=-1, source=None, trigger=None):
        """
        Constructs a control-rate SendReply.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> send_reply = supriya.ugens.SendReply.kr(
            ...     command_name="/reply",
            ...     source=source,
            ...     trigger=trigger,
            ... )
            >>> send_reply
            SendReply.kr()

        Returns ugen graph.
        """
        calculation_rate = CalculationRate.CONTROL
        ugen = cls._new_single(
            calculation_rate=calculation_rate,
            command_name=command_name,
            reply_id=reply_id,
            source=source,
            trigger=trigger,
        )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def command_name(self):
        """
        Gets `command_name` input of SendReply.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> send_reply = supriya.ugens.SendReply.ar(
            ...     command_name="/reply",
            ...     source=source,
            ...     trigger=trigger,
            ... )
            >>> send_reply.command_name
            '/reply'

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("reply_id") + 1
        size = int(self._inputs[index])
        command_name = "".join(
            [chr(int(_)) for _ in self._inputs[index + 1 : index + 1 + size]]
        )
        return command_name

    @property
    def source(self):
        """
        Gets `source` input of SendReply.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> send_reply = supriya.ugens.SendReply.ar(
            ...     command_name="/reply",
            ...     source=source,
            ...     trigger=trigger,
            ... )
            >>> send_reply.source
            (In.ar()[0], In.ar()[1], In.ar()[2], In.ar()[3])

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("reply_id") + 1
        size = int(self._inputs[index])
        return tuple(self._inputs[index + 1 + size :])


class SendTrig(UGen):
    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("id_", 0), ("value", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Sweep(UGen):
    """
    A triggered linear ramp.

    ::

        >>> sweep = supriya.ugens.Sweep.ar(
        ...     rate=1,
        ...     trigger=0,
        ... )
        >>> sweep
        Sweep.ar()

    """

    _ordered_input_names = collections.OrderedDict([("trigger", 0), ("rate", 1)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class TDelay(UGen):
    """
    A trigger delay.

    ::

        >>> source = supriya.ugens.Dust.kr()
        >>> tdelay = supriya.ugens.TDelay.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> tdelay
        TDelay.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("duration", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class ToggleFF(UGen):
    """
    A toggle flip-flop.

    ::

        >>> trigger = supriya.ugens.Dust.kr(1)
        >>> toggle_ff = supriya.ugens.ToggleFF.ar(
        ...     trigger=trigger,
        ... )
        >>> toggle_ff
        ToggleFF.ar()

    """

    _ordered_input_names = collections.OrderedDict([("trigger", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Trig1(UGen):
    """
    A timed trigger.

    ::

        >>> source = supriya.ugens.Dust.kr(1)
        >>> trig_1 = supriya.ugens.Trig1.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> trig_1
        Trig1.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("duration", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Trig(UGen):
    """
    A timed trigger.

    ::

        >>> source = supriya.ugens.Dust.kr(1)
        >>> trig = supriya.ugens.Trig.ar(
        ...     duration=0.1,
        ...     source=source,
        ... )
        >>> trig
        Trig.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("duration", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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
        Wrap.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", 0), ("minimum", 0), ("maximum", 1)]
    )
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


class ZeroCrossing(UGen):
    """
    A zero-crossing frequency follower.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> zero_crossing = supriya.ugens.ZeroCrossing.ar(
        ...     source=source,
        ... )
        >>> zero_crossing
        ZeroCrossing.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
