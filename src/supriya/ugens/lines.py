from typing import Any

from ..enums import CalculationRate, DoneAction
from .basic import MulAdd
from .core import PseudoUGen, UGen, UGenOperable, UGenVector, param, ugen


@ugen(kr=True, is_pure=True)
class A2K(UGen):
    """
    An audio-rate to control-rate convert unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> a_2_k = supriya.ugens.A2K.kr(
        ...     source=source,
        ... )
        >>> a_2_k
        <A2K.kr()[0]>
    """

    source = param()


@ugen(ar=True, ir=True, kr=True, is_pure=True)
class AmpComp(UGen):
    """
    Basic psychoacoustic amplitude compensation.

    ::

        >>> amp_comp = supriya.ugens.AmpComp.ar(
        ...     exp=0.3333,
        ...     frequency=1000,
        ...     root=0,
        ... )
        >>> amp_comp
        <AmpComp.ar()[0]>
    """

    frequency = param(1000.0)
    root = param(0.0)
    exp = param(0.3333)


@ugen(ar=True, ir=True, kr=True, is_pure=True)
class AmpCompA(UGen):
    """
    Basic psychoacoustic amplitude compensation (ANSI A-weighting curve).

    ::

        >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
        ...     frequency=1000,
        ...     min_amp=0.32,
        ...     root=0,
        ...     root_amp=1,
        ... )
        >>> amp_comp_a
        <AmpCompA.ar()[0]>
    """

    frequency = param(1000.0)
    root = param(0.0)
    min_amp = param(0.32)
    root_amp = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class DC(UGen):
    """
    A DC unit generator.

    ::

        >>> supriya.ugens.DC.ar(
        ...     source=0,
        ... )
        <DC.ar()[0]>

    ::

        >>> supriya.ugens.DC.ar(
        ...     source=(1, 2, 3),
        ... )
        <UGenVector([<DC.ar()[0]>, <DC.ar()[0]>, <DC.ar()[0]>])>
    """

    source = param()


@ugen(ar=True, is_pure=True)
class K2A(UGen):
    """
    A control-rate to audio-rate converter unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.kr()
        >>> k_2_a = supriya.ugens.K2A.ar(
        ...     source=source,
        ... )
        >>> k_2_a
        <K2A.ar()[0]>
    """

    source = param()


@ugen(ar=True, kr=True, is_pure=True)
class LinExp(UGen):
    """
    A linear-to-exponential range mapper.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> lin_exp = supriya.ugens.LinExp.ar(
        ...     input_maximum=1.0,
        ...     input_minimum=-1.0,
        ...     output_maximum=22050,
        ...     output_minimum=20,
        ...     source=source,
        ... )
        >>> lin_exp
        <LinExp.ar()[0]>
    """

    source = param()
    input_minimum = param(0)
    input_maximum = param(1)
    output_minimum = param(1)
    output_maximum = param(2)


class LinLin(PseudoUGen):
    @staticmethod
    def ar(
        *,
        source,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
    ) -> UGenOperable:
        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        return MulAdd.new(source=source, multiplier=scale, addend=offset)

    @staticmethod
    def kr(
        *,
        source,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
    ) -> UGenOperable:
        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        return MulAdd.new(source=source, multiplier=scale, addend=offset)


@ugen(ar=True, kr=True, has_done_flag=True)
class Line(UGen):
    """
    A line generating unit generator.

    ::

        >>> supriya.ugens.Line.ar()
        <Line.ar()[0]>
    """

    start = param(0.0)
    stop = param(1.0)
    duration = param(1.0)
    done_action = param(DoneAction(0))

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        return calculation_rate, {
            **kwargs,
            "done_action": DoneAction.from_expr(int(kwargs["done_action"])),
        }


class Silence(PseudoUGen):
    """
    An audio-rate silence pseudo-unit generator.

    ::

        >>> supriya.ugens.Silence.ar(channel_count=2)
        <UGenVector([<DC.ar()[0]>, <DC.ar()[0]>])>
    """

    @classmethod
    def ar(cls, channel_count=1):
        from . import DC

        channel_count = int(channel_count)
        silence = DC.ar(source=0)
        if channel_count == 1:
            return silence
        output_proxies = [silence] * channel_count
        return UGenVector(*output_proxies)


@ugen(ar=True, kr=True, has_done_flag=True)
class XLine(UGen):
    """
    An exponential line generating unit generator.

    ::

        >>> supriya.ugens.XLine.ar()
        <XLine.ar()[0]>
    """

    start = param(0.0)
    stop = param(0.0)
    duration = param(1.0)
    done_action = param(DoneAction(0))
