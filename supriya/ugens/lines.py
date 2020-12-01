import abc
import collections

from supriya import CalculationRate
from supriya.synthdefs import PseudoUGen, PureUGen, UGen


class A2K(PureUGen):
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

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class AmpComp(PureUGen):
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

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 1000), ("root", 0), ("exp", 0.3333)]
    )
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


class AmpCompA(PureUGen):
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

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 1000), ("root", 0), ("min_amp", 0.32), ("root_amp", 1)]
    )
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


class DC(PureUGen):
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

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class K2A(PureUGen):
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

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class LinExp(PureUGen):
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

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("input_minimum", 0),
            ("input_maximum", 1),
            ("output_minimum", 1),
            ("output_maximum", 2),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LinLin(PseudoUGen):

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @staticmethod
    def ar(
        source=None,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
    ):
        import supriya.ugens

        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        ugen = supriya.ugens.MulAdd.new(source=source, multiplier=scale, addend=offset)
        return ugen

    @staticmethod
    def kr(
        source=None,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
    ):
        import supriya.ugens

        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        ugen = supriya.ugens.MulAdd.new(source=source, multiplier=scale, addend=offset)
        return ugen


class Line(UGen):
    """
    A line generating unit generator.

    ::

        >>> supriya.ugens.Line.ar()
        Line.ar()

    """

    ### CLASS VARIABLES ###

    _has_done_flag = True
    _ordered_input_names = collections.OrderedDict(
        [("start", 0.0), ("stop", 1.0), ("duration", 1.0), ("done_action", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        calculation_rate=None,
        done_action=None,
        duration=None,
        stop=None,
        start=None,
    ):
        import supriya.synthdefs

        done_action = supriya.DoneAction.from_expr(int(done_action))
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
        import supriya.synthdefs
        import supriya.ugens

        channel_count = int(channel_count)
        assert 0 <= channel_count
        silence = supriya.ugens.DC.ar(0)
        if channel_count == 1:
            return silence
        output_proxies = [silence[0]] * channel_count
        return supriya.synthdefs.UGenArray(output_proxies)


class XLine(UGen):
    """
    An exponential line generating unit generator.

    ::

        >>> supriya.ugens.XLine.ar()
        XLine.ar()

    """

    _has_done_flag = True
    _ordered_input_names = collections.OrderedDict(
        [("start", 0.0), ("stop", 1.0), ("duration", 1.0), ("done_action", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
