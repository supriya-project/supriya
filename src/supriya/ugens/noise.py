from typing import Any

from ..enums import CalculationRate, SignalRange
from .core import UGen, param, ugen


@ugen(ar=True, kr=True)
class BrownNoise(UGen):
    """
    A brown noise unit generator.

    ::

        >>> supriya.ugens.BrownNoise.ar()
        <BrownNoise.ar()[0]>
    """


@ugen(ar=True, kr=True)
class ClipNoise(UGen):
    """
    A clipped noise unit generator.

    ::

        >>> supriya.ugens.ClipNoise.ar()
        <ClipNoise.ar()[0]>
    """


@ugen(ar=True, kr=True)
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
        <CoinGate.ar()[0]>
    """

    probability = param(0.5)
    trigger = param()


@ugen(ar=True, kr=True)
class Crackle(UGen):
    """
    A chaotic noise generator.

    ::

        >>> crackle = supriya.ugens.Crackle.ar(
        ...     chaos_parameter=1.25,
        ... )
        >>> crackle
        <Crackle.ar()[0]>
    """

    chaos_parameter = param(1.5)


@ugen(ar=True, kr=True, signal_range=SignalRange.UNIPOLAR)
class Dust(UGen):
    """
    A unipolar random impulse generator.

    ::

        >>> dust = supriya.ugens.Dust.ar(
        ...     density=23,
        ... )
        >>> dust
        <Dust.ar()[0]>
    """

    density = param(0.0)


@ugen(ar=True, kr=True)
class Dust2(UGen):
    """
    A bipolar random impulse generator.

    ::

        >>> dust_2 = supriya.ugens.Dust2.ar(
        ...     density=23,
        ... )
        >>> dust_2
        <Dust2.ar()[0]>
    """

    density = param(0.0)


@ugen(ir=True)
class ExpRand(UGen):
    """
    An exponential random distribution.

    ::

        >>> exp_rand = supriya.ugens.ExpRand.ir()
        >>> exp_rand
        <ExpRand.ir()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        if isinstance(kwargs["minimum"], float) and isinstance(
            kwargs["maximum"], float
        ):
            kwargs["minimum"], kwargs["maximum"] = sorted(
                [kwargs["minimum"], kwargs["maximum"]]
            )
        return calculation_rate, kwargs


@ugen(ar=True, kr=True)
class GrayNoise(UGen):
    """
    A gray noise unit generator.

    ::

        >>> supriya.ugens.GrayNoise.ar()
        <GrayNoise.ar()[0]>
    """


@ugen(ar=True, kr=True)
class Hasher(UGen):
    """
    A signal hasher.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> hasher = supriya.ugens.Hasher.ar(
        ...     source=source,
        ... )
        >>> hasher
        <Hasher.ar()[0]>
    """

    source = param()


@ugen(ir=True)
class IRand(UGen):
    """
    An integer uniform random distribution.

    ::

        >>> supriya.ugens.IRand.ir()
        <IRand.ir()[0]>
    """

    minimum = param(0)
    maximum = param(127)


@ugen(ar=True, kr=True)
class LFClipNoise(UGen):
    """
    A dynamic clipped noise generator.

    ::

        >>> supriya.ugens.LFClipNoise.ar()
        <LFClipNoise.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFDClipNoise(UGen):
    """
    A clipped noise generator.

    ::

        >>> supriya.ugens.LFDClipNoise.ar()
        <LFDClipNoise.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFDNoise0(UGen):
    """
    A dynamic step noise generator.

    ::

        >>> supriya.ugens.LFDNoise0.ar()
        <LFDNoise0.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFDNoise1(UGen):
    """
    A dynamic ramp noise generator.

    ::

        >>> supriya.ugens.LFDNoise1.ar()
        <LFDNoise1.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFDNoise3(UGen):
    """
    A dynamic polynomial noise generator.

    ::

        >>> supriya.ugens.LFDNoise3.ar()
        <LFDNoise3.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFNoise0(UGen):
    """
    A step noise generator.

    ::

        >>> supriya.ugens.LFNoise0.ar()
        <LFNoise0.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFNoise1(UGen):
    """
    A ramp noise generator.

    ::

        >>> supriya.ugens.LFNoise1.ar()
        <LFNoise1.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ar=True, kr=True)
class LFNoise2(UGen):
    """
    A quadratic noise generator.

    ::

        >>> supriya.ugens.LFNoise2.ar()
        <LFNoise2.ar()[0]>
    """

    frequency = param(500.0)


@ugen(ir=True)
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
        <LinRand.ir()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    skew = param(0)


@ugen(ar=True, kr=True)
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
        <Logistic.ar()[0]>
    """

    chaos_parameter = param(3)
    frequency = param(1000)
    initial_y = param(0.5)


@ugen(ar=True, kr=True)
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
        <MantissaMask.ar()[0]>
    """

    source = param(0)
    bits = param(3)


@ugen(ir=True)
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
        <NRand.ir()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    n = param(1)


@ugen(ar=True, kr=True)
class PinkNoise(UGen):
    """
    A pink noise unit generator.

    ::

        >>> supriya.ugens.PinkNoise.ar()
        <PinkNoise.ar()[0]>
    """


@ugen(ir=True)
class Rand(UGen):
    """
    A uniform random distribution.

    ::

        >>> supriya.ugens.Rand.ir()
        <Rand.ir()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)


@ugen(kr=True, ir=True, is_width_first=True)
class RandID(UGen):
    """
    Sets the synth's random generator ID.

    ::

        >>> rand_id = supriya.ugens.RandID.ir(
        ...     rand_id=1,
        ... )
        >>> rand_id
        <RandID.ir()[0]>
    """

    rand_id = param(1)


@ugen(ar=True, kr=True, ir=True, is_width_first=True)
class RandSeed(UGen):
    """
    Sets the synth's random generator seed.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> rand_seed = supriya.ugens.RandSeed.ar(
        ...     seed=1,
        ...     trigger=trigger,
        ... )
        >>> rand_seed
        <RandSeed.ar()[0]>
    """

    trigger = param(0)
    seed = param(56789)


@ugen(ar=True, kr=True)
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
        <TExpRand.ar()[0]>
    """

    minimum = param(0.01)
    maximum = param(1.0)
    trigger = param(0)


@ugen(ar=True, kr=True)
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
        <TIRand.ar()[0]>
    """

    minimum = param(0)
    maximum = param(127)
    trigger = param(0)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        kwargs["minimum"] = int(kwargs["minimum"])
        kwargs["maximum"] = int(kwargs["maximum"])
        return calculation_rate, kwargs


@ugen(ar=True, kr=True)
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
        <TRand.ar()[0]>
    """

    minimum = param(0.0)
    maximum = param(1.0)
    trigger = param(0)


@ugen(ar=True, kr=True)
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
        <TWindex.ar()[0]>
    """

    trigger = param()
    normalize = param(0)
    array = param(unexpanded=True)


@ugen(ar=True, kr=True)
class WhiteNoise(UGen):
    """
    A white noise unit generator.

    ::

        >>> supriya.ugens.WhiteNoise.ar()
        <WhiteNoise.ar()[0]>
    """
