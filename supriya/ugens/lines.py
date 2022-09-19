from supriya import DoneAction

from .bases import PseudoUGen, UGen, UGenArray, param, ugen
from .basic import MulAdd


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
        A2K.kr()

    """

    source = param(None)


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
        AmpComp.ar()

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
        AmpCompA.ar()

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
        DC.ar()

    ::

        >>> supriya.ugens.DC.ar(
        ...     source=(1, 2, 3),
        ... )
        UGenArray({3})

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
        K2A.ar()

    """

    source = param(None)


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
        LinExp.ar()

    """

    source = param(None)
    input_minimum = param(0)
    input_maximum = param(1)
    output_minimum = param(1)
    output_maximum = param(2)


class LinLin(PseudoUGen):
    @staticmethod
    def ar(
        source=None,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
    ):
        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        ugen = MulAdd.new(source=source, multiplier=scale, addend=offset)
        return ugen

    @staticmethod
    def kr(
        source=None,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
    ):
        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        ugen = MulAdd.new(source=source, multiplier=scale, addend=offset)
        return ugen


@ugen(ar=True, kr=True, has_done_flag=True)
class Line(UGen):
    """
    A line generating unit generator.

    ::

        >>> supriya.ugens.Line.ar()
        Line.ar()

    """

    start = param(0.0)
    stop = param(1.0)
    duration = param(1.0)
    done_action = param(DoneAction(0))

    @classmethod
    def _new_expanded(
        cls,
        calculation_rate=None,
        done_action=None,
        duration=None,
        stop=None,
        start=None,
    ):
        done_action = DoneAction.from_expr(int(done_action))
        return super(Line, cls)._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            stop=stop,
            start=start,
        )


class Silence(PseudoUGen):
    """
    An audio-rate silence pseudo-unit generator.

    ::

        >>> supriya.ugens.Silence.ar(channel_count=2)
        UGenArray({2})

    """

    @classmethod
    def ar(cls, channel_count=1):
        from . import DC

        channel_count = int(channel_count)
        assert 0 <= channel_count
        silence = DC.ar(source=0)
        if channel_count == 1:
            return silence
        output_proxies = [silence[0]] * channel_count
        return UGenArray(output_proxies)


@ugen(ar=True, kr=True, has_done_flag=True)
class XLine(UGen):
    """
    An exponential line generating unit generator.

    ::

        >>> supriya.ugens.XLine.ar()
        XLine.ar()

    """

    start = param(0.0)
    stop = param(0.0)
    duration = param(1.0)
    done_action = param(DoneAction(0))
