from collections.abc import Sequence

from supriya import utils

from .bases import UGen, param, ugen


@ugen(ar=True, kr=True, is_input=True, is_multichannel=True)
class In(UGen):
    """
    A bus input unit generator.

    ::

        >>> supriya.ugens.In.ar(bus=0, channel_count=4)
        UGenArray({4})

    """

    bus = param(0.0)


@ugen(ar=True, kr=True, is_input=True, is_multichannel=True)
class InFeedback(UGen):
    """
    A bus input unit generator.

    Reads signal from a bus with a current or one cycle old timestamp.

    ::

        >>> in_feedback = supriya.ugens.InFeedback.ar(
        ...     bus=0,
        ...     channel_count=2,
        ... )
        >>> in_feedback
        UGenArray({2})

    """

    bus = param(0.0)


@ugen(ar=True, kr=True, is_multichannel=True)
class LocalIn(UGen):
    """
    A SynthDef-local bus input.

    ::

        >>> supriya.ugens.LocalIn.ar(channel_count=2)
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    default = param(0.0, unexpanded=True)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, channel_count=1, default=0):
        self._channel_count = int(channel_count)
        if not isinstance(default, Sequence):
            default = (default,)
        default = (float(_) for _ in default)
        default = utils.repeat_sequence_to_length(default, channel_count)
        default = list(default)[:channel_count]
        UGen.__init__(self, calculation_rate=calculation_rate, default=default)


@ugen(ar=True, kr=True, channel_count=0, fixed_channel_count=True)
class LocalOut(UGen):
    """
    A SynthDef-local bus output.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.LocalOut.ar(
        ...     source=source,
        ... )
        LocalOut.ar()

    """

    source = param(None, unexpanded=True)


@ugen(ar=True, kr=True, is_output=True, channel_count=0, fixed_channel_count=True)
class OffsetOut(UGen):
    """
    A bus output unit generator with sample-accurate timing.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.OffsetOut.ar(
        ...     bus=0,
        ...     source=source,
        ... )
        OffsetOut.ar()

    """

    bus = param(0)
    source = param(None, unexpanded=True)


@ugen(ar=True, kr=True, is_output=True, channel_count=0, fixed_channel_count=True)
class Out(UGen):
    """
    A bus output unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.Out.ar(
        ...     bus=0,
        ...     source=source,
        ... )
        Out.ar()

    """

    bus = param(0)
    source = param(None, unexpanded=True)


@ugen(ar=True, kr=True, is_output=True, channel_count=0, fixed_channel_count=True)
class ReplaceOut(UGen):
    """
    An overwriting bus output unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.ReplaceOut.ar(
        ...     bus=0,
        ...     source=source,
        ... )
        ReplaceOut.ar()

    """

    bus = param(0)
    source = param(None, unexpanded=True)


@ugen(ar=True, kr=True, is_output=True, channel_count=0, fixed_channel_count=True)
class XOut(UGen):
    """
    A cross-fading bus output unit generator.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> xout = supriya.ugens.XOut.ar(
        ...     bus=0,
        ...     crossfade=0.5,
        ...     source=source,
        ... )
        >>> xout
        XOut.ar()

    """

    bus = param(0)
    crossfade = param(0.0)
    source = param(None, unexpanded=True)
