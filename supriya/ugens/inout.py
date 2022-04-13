import collections
from collections.abc import Sequence

from supriya import CalculationRate, utils
from supriya.synthdefs import MultiOutUGen, UGen


class In(MultiOutUGen):
    """
    A bus input unit generator.

    ::

        >>> supriya.ugens.In.ar(bus=0, channel_count=4)
        UGenArray({4})

    """

    _default_channel_count = 1
    _has_settable_channel_count = True
    _is_input = True
    _ordered_input_names = collections.OrderedDict([("bus", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class InFeedback(MultiOutUGen):
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

    _default_channel_count = 1
    _has_settable_channel_count = True
    _is_input = True
    _ordered_input_names = collections.OrderedDict([("bus", 0)])
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LocalIn(MultiOutUGen):
    """
    A SynthDef-local bus input.

    ::

        >>> supriya.ugens.LocalIn.ar(channel_count=2)
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict([("default", 0)])
    _unexpanded_input_names = ("default",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, channel_count=1, default=0):
        if not isinstance(default, Sequence):
            default = (default,)
        default = (float(_) for _ in default)
        default = utils.repeat_sequence_to_length(default, channel_count)
        default = list(default)[:channel_count]
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
        )


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

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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

    _default_channel_count = 0
    _is_output = True
    _ordered_input_names = collections.OrderedDict([("bus", 0), ("source", None)])
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO,)


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

    _default_channel_count = 0
    _is_output = True
    _ordered_input_names = collections.OrderedDict([("bus", 0.0), ("source", None)])
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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

    _default_channel_count = 0
    _is_output = True
    _ordered_input_names = collections.OrderedDict([("bus", 0), ("source", None)])
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


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

    _default_channel_count = 0
    _is_output = True
    _ordered_input_names = collections.OrderedDict(
        [("bus", 0), ("crossfade", 0), ("source", None)]
    )
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
