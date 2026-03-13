from typing import Any, Sequence

from ..enums import CalculationRate
from ..utils import repeat_to_length
from .core import UGen, param, ugen


@ugen(ar=True, kr=True, is_input=True, is_multichannel=True)
class In(UGen):
    """
    A bus input unit generator.

    ::

        >>> supriya.ugens.In.ar(bus=0, channel_count=4)
        <In.ar()>
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
        <InFeedback.ar()>
    """

    bus = param(0.0)


@ugen(ar=True, kr=True, is_multichannel=True)
class LocalIn(UGen):
    """
    A SynthDef-local bus input.

    ::

        >>> supriya.ugens.LocalIn.ar(channel_count=2)
        <LocalIn.ar()>
    """

    default = param(0.0, unexpanded=True)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        default = kwargs["default"]
        if not isinstance(default, Sequence):
            default = [default]
        kwargs["default"] = list(
            repeat_to_length([float(x) for x in default], self._channel_count)
        )
        return calculation_rate, kwargs


@ugen(ar=True, kr=True, channel_count=0, fixed_channel_count=True)
class LocalOut(UGen):
    """
    A SynthDef-local bus output.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.LocalOut.ar(
        ...     source=source,
        ... )
        <LocalOut.ar()>
    """

    source = param(unexpanded=True)


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
        <OffsetOut.ar()>
    """

    bus = param(0)
    source = param(unexpanded=True)


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
        <Out.ar()>
    """

    bus = param(0)
    source = param(unexpanded=True)


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
        <ReplaceOut.ar()>
    """

    bus = param(0)
    source = param(unexpanded=True)


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
        <XOut.ar()>
    """

    bus = param(0)
    crossfade = param(0.0)
    source = param(unexpanded=True)
