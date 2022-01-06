import collections

from supriya import CalculationRate
from supriya.synthdefs import PseudoUGen, PureUGen


class Filter(PureUGen):
    """
    Abstract base class for filter ugens.
    """

    def _validate_inputs(self):
        self._check_rate_same_as_first_input_rate()


class APF(Filter):
    """
    An all-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> apf = supriya.ugens.APF.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ... )
        >>> apf
        APF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440.0), ("radius", 0.8)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BPF(Filter):
    """
    A 2nd order Butterworth bandpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_p_f = supriya.ugens.BPF.ar(source=source)
        >>> b_p_f
        BPF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440.0), ("reciprocal_of_q", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BPZ2(Filter):
    """
    A two zero fixed midpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bpz_2 = supriya.ugens.BPZ2.ar(
        ...     source=source,
        ... )
        >>> bpz_2
        BPZ2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BRF(Filter):
    """
    A 2nd order Butterworth band-reject filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_r_f = supriya.ugens.BRF.ar(source=source)
        >>> b_r_f
        BRF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440.0), ("reciprocal_of_q", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BRZ2(Filter):
    """
    A two zero fixed midcut filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> brz_2 = supriya.ugens.BRZ2.ar(
        ...     source=source,
        ... )
        >>> brz_2
        BRZ2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Changed(PseudoUGen):
    """
    Triggers when a value changes.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> changed = supriya.ugens.Changed.ar(
        ...     source=source,
        ...     threshold=0,
        ... )
        >>> supriya.graph(changed)  # doctest: +SKIP

    ::

        >>> print(changed)
        synthdef:
            name: 39e1f9d61589c4acaaf297cc961d65e4
            ugens:
            -   In.ar:
                    bus: 0.0
            -   HPZ1.ar:
                    source: In.ar[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).ar:
                    source: HPZ1.ar[0]
            -   BinaryOpUGen(GREATER_THAN).ar:
                    left: UnaryOpUGen(ABSOLUTE_VALUE).ar[0]
                    right: 0.0

    """

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, source=None, threshold=0):
        """
        Constructs an audio-rate Changed.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> changed = supriya.ugens.Changed.ar(
            ...     source=source,
            ...     threshold=0,
            ... )
            >>> supriya.graph(changed)  # doctest: +SKIP

        ::

            >>> print(changed)
            synthdef:
                name: 39e1f9d61589c4acaaf297cc961d65e4
                ugens:
                -   In.ar:
                        bus: 0.0
                -   HPZ1.ar:
                        source: In.ar[0]
                -   UnaryOpUGen(ABSOLUTE_VALUE).ar:
                        source: HPZ1.ar[0]
                -   BinaryOpUGen(GREATER_THAN).ar:
                        left: UnaryOpUGen(ABSOLUTE_VALUE).ar[0]
                        right: 0.0

        Returns ugen graph.
        """
        import supriya.ugens

        ugen = abs(supriya.ugens.HPZ1.ar(source=source)) > threshold
        return ugen

    @classmethod
    def kr(cls, source=None, threshold=0):
        """
        Constructs a control-rate Changed.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> changed = supriya.ugens.Changed.kr(
            ...     source=source,
            ...     threshold=0,
            ... )
            >>> supriya.graph(changed)  # doctest: +SKIP

        ::

            >>> print(changed)
            synthdef:
                name: e2436271176995c6a0a5cac6d1553f8b
                ugens:
                -   In.ar:
                        bus: 0.0
                -   HPZ1.kr:
                        source: In.ar[0]
                -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                        source: HPZ1.kr[0]
                -   BinaryOpUGen(GREATER_THAN).kr:
                        left: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                        right: 0.0

        Returns ugen graph.
        """
        import supriya.ugens

        ugen = abs(supriya.ugens.HPZ1.kr(source=source)) > threshold
        return ugen


class Decay(Filter):
    """
    A leaky signal integrator.

    ::

        >>> source = supriya.ugens.Impulse.ar()
        >>> decay = supriya.ugens.Decay.ar(
        ...     source=source,
        ... )
        >>> decay
        Decay.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("decay_time", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Decay2(Filter):
    """
    A leaky signal integrator.

    ::

        >>> source = supriya.ugens.Impulse.ar()
        >>> decay_2 = supriya.ugens.Decay2.ar(
        ...     source=source,
        ... )
        >>> decay_2
        Decay2.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("attack_time", 0.01), ("decay_time", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DetectSilence(Filter):
    """
    Evaluates `done_action` when input falls below `threshold`.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> source *= supriya.ugens.Line.kr(start=1, stop=0)
        >>> detect_silence = supriya.ugens.DetectSilence.kr(
        ...     done_action=supriya.DoneAction.FREE_SYNTH,
        ...     source=source,
        ...     threshold=0.0001,
        ...     time=1.0,
        ... )
        >>> detect_silence
        DetectSilence.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("threshold", 0.0001), ("time", 0.1), ("done_action", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### PRIVATE METHODS ###

    def _optimize_graph(self, sort_bundles):
        # TODO: Replace with `_is_pure = False` class variable
        pass


class FOS(Filter):
    """
    A first order filter section.

    ::

        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (a2 * in(i-2)) + (b1 * out(i-1)) + (b2 * out(i-2))

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> fos = supriya.ugens.FOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     b_1=0,
        ...     source=source,
        ... )
        >>> fos
        FOS.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("a_0", 0.0), ("a_1", 0.0), ("b_1", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Formlet(Filter):
    """
    A FOF-like filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> formlet = supriya.ugens.Formlet.ar(
        ...     attack_time=1,
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ... )
        >>> formlet
        Formlet.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("frequency", 440.0),
            ("attack_time", 1.0),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class HPF(Filter):
    """
    A Highpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.HPF.ar(source=source)
        HPF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class HPZ1(Filter):
    """
    A two point difference filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_1 = supriya.ugens.HPZ1.ar(
        ...     source=source,
        ... )
        >>> hpz_1
        HPZ1.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class HPZ2(Filter):
    """
    A two zero fixed midcut filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_2 = supriya.ugens.HPZ2.ar(
        ...     source=source,
        ... )
        >>> hpz_2
        HPZ2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Integrator(Filter):
    """
    A leaky integrator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> integrator = supriya.ugens.Integrator.ar(
        ...     coefficient=1,
        ...     source=source,
        ... )
        >>> integrator
        Integrator.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Lag(Filter):
    """
    A lag generator.

    ::

        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.Lag.kr(
        ...     lag_time=0.5,
        ...     source=source,
        ... )
        Lag.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LagUD(Filter):
    """
    An up/down lag generator.

    ::

        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.LagUD.kr(
        ...     lag_time_down=1.25,
        ...     lag_time_up=0.5,
        ...     source=source,
        ... )
        LagUD.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time_up", 0.1), ("lag_time_down", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Lag2(Filter):
    """
    An exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_2 = supriya.ugens.Lag2.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ... )
        >>> lag_2
        Lag2.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Lag2UD(Filter):
    """
    An up/down exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_2_ud = supriya.ugens.Lag2UD.ar(
        ...     lag_time_d=0.1,
        ...     lag_time_u=0.1,
        ...     source=source,
        ... )
        >>> lag_2_ud
        Lag2UD.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time_u", 0.1), ("lag_time_d", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Lag3(Filter):
    """
    An exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3 = supriya.ugens.Lag3.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ... )
        >>> lag_3
        Lag3.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Lag3UD(Filter):
    """
    An up/down exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3_ud = supriya.ugens.Lag3UD.ar(
        ...     lag_time_d=0.1,
        ...     lag_time_u=0.1,
        ...     source=source,
        ... )
        >>> lag_3_ud
        Lag3UD.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time_u", 0.1), ("lag_time_d", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LeakDC(Filter):
    """
    A DC blocker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> leak_d_c = supriya.ugens.LeakDC.ar(
        ...     source=source,
        ...     coefficient=0.995,
        ... )
        >>> leak_d_c
        LeakDC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 0.995)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LPF(Filter):
    """
    A lowpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.LPF.ar(source=source)
        LPF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LPZ1(Filter):
    """
    A two point average filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lpz_1 = supriya.ugens.LPZ1.ar(
        ...     source=source,
        ... )
        >>> lpz_1
        LPZ1.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LPZ2(Filter):
    """
    A two zero fixed lowpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lpz_2 = supriya.ugens.LPZ2.ar(
        ...     source=source,
        ... )
        >>> lpz_2
        LPZ2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Median(Filter):
    """
    A median filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> median = supriya.ugens.Median.ar(
        ...     length=3,
        ...     source=source,
        ... )
        >>> median
        Median.ar()

    """

    _ordered_input_names = collections.OrderedDict([("length", 3), ("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class MidEQ(Filter):
    """
    A parametric filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> mid_eq = supriya.ugens.MidEQ.ar(
        ...     db=0,
        ...     frequency=440,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> mid_eq
        MidEQ.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("reciprocal_of_q", 1), ("db", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class MoogFF(Filter):
    """
    A Moog VCF implementation.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> moog_ff = supriya.ugens.MoogFF.ar(
        ...     frequency=100,
        ...     gain=2,
        ...     reset=0,
        ...     source=source,
        ... )
        >>> moog_ff
        MoogFF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 100), ("gain", 2), ("reset", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class OnePole(Filter):
    """
    A one pole filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> one_pole = supriya.ugens.OnePole.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ... )
        >>> one_pole
        OnePole.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class OneZero(Filter):
    """
    A one zero filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> one_zero = supriya.ugens.OneZero.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ... )
        >>> one_zero
        OneZero.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("coefficient", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class RHPF(Filter):
    """
    A resonant highpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.RLPF.ar(source=source)
        RLPF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("reciprocal_of_q", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class RLPF(Filter):
    """
    A resonant lowpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.RLPF.ar(source=source)
        RLPF.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("reciprocal_of_q", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Ramp(Filter):
    """
    Breaks a continuous signal into line segments.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ramp = supriya.ugens.Ramp.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ... )
        >>> ramp
        Ramp.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("lag_time", 0.1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Ringz(Filter):
    """
    A ringing filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ringz = supriya.ugens.Ringz.ar(
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ... )
        >>> ringz
        Ringz.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("decay_time", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class SOS(Filter):
    """
    A second-order filter section.

    ::

        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (b1 * out(i-1))

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> sos = supriya.ugens.SOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     a_2=0,
        ...     b_1=0,
        ...     b_2=0,
        ...     source=source,
        ... )
        >>> sos
        SOS.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("a_0", 0), ("a_1", 0), ("a_2", 0), ("b_1", 0), ("b_2", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Slew(Filter):
    """
    A slew rate limiter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slew = supriya.ugens.Slew.ar(
        ...     source=source,
        ...     up=1,
        ...     down=1,
        ... )
        >>> slew
        Slew.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("up", 1), ("down", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Slope(Filter):
    """
    Calculates slope of signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slope = supriya.ugens.Slope.ar(
        ...     source=source,
        ... )
        >>> slope
        Slope.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class TwoPole(Filter):
    """
    A two pole filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_pole = supriya.ugens.TwoPole.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ... )
        >>> two_pole
        TwoPole.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("radius", 0.8)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class TwoZero(Filter):
    """
    A two zero filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> two_zero = supriya.ugens.TwoZero.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ... )
        >>> two_zero
        TwoZero.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("radius", 0.8)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
