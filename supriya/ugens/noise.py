import collections

from supriya import CalculationRate, SignalRange
from supriya.synthdefs import UGen, WidthFirstUGen
from supriya.typing import UGenInputMap


class BrownNoise(UGen):
    """
    A brown noise unit generator.

    ::

        >>> supriya.ugens.BrownNoise.ar()
        BrownNoise.ar()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class ClipNoise(UGen):
    """
    A clipped noise unit generator.

    ::

        >>> supriya.ugens.ClipNoise.ar()
        ClipNoise.ar()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class CoinGate(UGen):
    """
    A probabilistic trigger gate.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> coin_gate = supriya.ugens.CoinGate.ar(
        ...     probability=0.5,
        ...     trigger=trigger,
        ... )
        >>> coin_gate
        CoinGate.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("probability", 0.5), ("trigger", None)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Crackle(UGen):
    """
    A chaotic noise generator.

    ::

        >>> crackle = supriya.ugens.Crackle.ar(
        ...     chaos_parameter=1.25,
        ... )
        >>> crackle
        Crackle.ar()

    """

    _ordered_input_names = collections.OrderedDict([("chaos_parameter", 1.5)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Dust(UGen):
    """
    A unipolar random impulse generator.

    ::

        >>> dust = supriya.ugens.Dust.ar(
        ...     density=23,
        ... )
        >>> dust
        Dust.ar()

    """

    _ordered_input_names = collections.OrderedDict([("density", 0.0)])
    _signal_range = SignalRange.UNIPOLAR
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Dust2(UGen):
    """
    A bipolar random impulse generator.

    ::

        >>> dust_2 = supriya.ugens.Dust2.ar(
        ...     density=23,
        ... )
        >>> dust_2
        Dust2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("density", 0.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class ExpRand(UGen):
    """
    An exponential random distribution.

    ::

        >>> exp_rand = supriya.ugens.ExpRand.ir()
        >>> exp_rand
        ExpRand.ir()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("minimum", 0.0), ("maximum", 1.0)])
    _valid_calculation_rates = (CalculationRate.SCALAR,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, maximum=None, minimum=None):
        minimum, maximum = sorted([minimum, maximum])
        UGen.__init__(
            self, calculation_rate=calculation_rate, minimum=minimum, maximum=maximum
        )


class GrayNoise(UGen):
    """
    A gray noise unit generator.

    ::

        >>> supriya.ugens.GrayNoise.ar()
        GrayNoise.ar()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Hasher(UGen):
    """
    A signal hasher.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> hasher = supriya.ugens.Hasher.ar(
        ...     source=source,
        ... )
        >>> hasher
        Hasher.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class IRand(UGen):
    """
    An integer uniform random distribution.

    ::

        >>> supriya.ugens.IRand.ir()
        IRand.ir()

    """

    _ordered_input_names = collections.OrderedDict([("minimum", 0), ("maximum", 127)])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class LFClipNoise(UGen):
    """
    A dynamic clipped noise generator.

    ::

        >>> supriya.ugens.LFClipNoise.ar()
        LFClipNoise.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFDClipNoise(UGen):
    """
    A clipped noise generator.

    ::

        >>> supriya.ugens.LFDClipNoise.ar()
        LFDClipNoise.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFDNoise0(UGen):
    """
    A dynamic step noise generator.

    ::

        >>> supriya.ugens.LFDNoise0.ar()
        LFDNoise0.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFDNoise1(UGen):
    """
    A dynamic ramp noise generator.

    ::

        >>> supriya.ugens.LFDNoise1.ar()
        LFDNoise1.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFDNoise3(UGen):
    """
    A dynamic polynomial noise generator.

    ::

        >>> supriya.ugens.LFDNoise3.ar()
        LFDNoise3.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFNoise0(UGen):
    """
    A step noise generator.

    ::

        >>> supriya.ugens.LFNoise0.ar()
        LFNoise0.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFNoise1(UGen):
    """
    A ramp noise generator.

    ::

        >>> supriya.ugens.LFNoise1.ar()
        LFNoise1.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFNoise2(UGen):
    """
    A quadratic noise generator.

    ::

        >>> supriya.ugens.LFNoise2.ar()
        LFNoise2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LinRand(UGen):
    """
    A skewed linear random distribution.

    ::

        >>> lin_rand = supriya.ugens.LinRand.ir(
        ...     minimum=-1.0,
        ...     maximum=1.0,
        ...     skew=0.5,
        ... )
        >>> lin_rand
        LinRand.ir()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("skew", 0)]
    )
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class Logistic(UGen):
    """
    A chaotic noise function.

    ::

        >>> logistic = supriya.ugens.Logistic.ar(
        ...     chaos_parameter=3.0,
        ...     frequency=1000,
        ...     initial_y=0.5,
        ... )
        >>> logistic
        Logistic.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("chaos_parameter", 3), ("frequency", 1000), ("initial_y", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class MantissaMask(UGen):
    """
    A floating-point mantissa mask.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
        ...     source=source,
        ...     bits=3,
        ... )
        >>> mantissa_mask
        MantissaMask.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", 0), ("bits", 3)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class NRand(UGen):
    """
    A sum of `n` uniform distributions.

    ::

        >>> n_rand = supriya.ugens.NRand.ir(
        ...     minimum=-1,
        ...     maximum=1,
        ...     n=1,
        ... )
        >>> n_rand
        NRand.ir()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.0), ("maximum", 1.0), ("n", 1)]
    )
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class PinkNoise(UGen):
    """
    A pink noise unit generator.

    ::

        >>> supriya.ugens.PinkNoise.ar()
        PinkNoise.ar()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Rand(UGen):
    """
    A uniform random distribution.

    ::

        >>> supriya.ugens.Rand.ir()
        Rand.ir()

    """

    _ordered_input_names = collections.OrderedDict([("minimum", 0.0), ("maximum", 1.0)])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class RandID(WidthFirstUGen):
    """
    Sets the synth's random generator ID.

    ::

        >>> rand_id = supriya.ugens.RandID.ir(
        ...     rand_id=1,
        ... )
        >>> rand_id
        RandID.ir()

    """

    _ordered_input_names = collections.OrderedDict([("rand_id", 1)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class RandSeed(WidthFirstUGen):
    """
    Sets the synth's random generator seed.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> rand_seed = supriya.ugens.RandSeed.ar(
        ...     seed=1,
        ...     trigger=trigger,
        ... )
        >>> rand_seed
        RandSeed.ar()

    """

    _ordered_input_names = collections.OrderedDict([("trigger", 0), ("seed", 56789)])
    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )


class TExpRand(UGen):
    """
    A triggered exponential random number generator.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_exp_rand = supriya.ugens.TExpRand.ar(
        ...     minimum=-1.0,
        ...     maximum=1.0,
        ...     trigger=trigger,
        ... )
        >>> t_exp_rand
        TExpRand.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0.01), ("maximum", 1), ("trigger", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class TIRand(UGen):
    """
    A triggered integer random number generator.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_i_rand = supriya.ugens.TIRand.ar(
        ...     minimum=0,
        ...     maximum=127,
        ...     trigger=trigger,
        ... )
        >>> t_i_rand
        TIRand.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 127), ("trigger", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, maximum=127, minimum=0, trigger=0):
        minimum = int(minimum)
        maximum = int(maximum)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            trigger=trigger,
        )


class TRand(UGen):
    """
    A triggered random number generator.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_rand = supriya.ugens.TRand.ar(
        ...     minimum=-1.0,
        ...     maximum=1.0,
        ...     trigger=trigger,
        ... )
        >>> t_rand
        TRand.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 1), ("trigger", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class TWindex(UGen):
    """
    A triggered windex.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_windex = supriya.ugens.TWindex.ar(
        ...     trigger=trigger,
        ...     normalize=0,
        ...     array=[1, 2, 3],
        ... )
        >>> t_windex
        TWindex.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("normalize", 0), ("array", None)]
    )
    _unexpanded_input_names = ("array",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class WhiteNoise(UGen):
    """
    A white noise unit generator.

    ::

        >>> supriya.ugens.WhiteNoise.ar()
        WhiteNoise.ar()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
