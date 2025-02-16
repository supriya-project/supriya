import math

from ..enums import CalculationRate
from .basic import Mix
from .core import (
    PseudoUGen,
    UGen,
    UGenOperable,
    UGenRecursiveParams,
    UGenVector,
    _get_method_for_rate,
    param,
    ugen,
)


@ugen(ar=True, kr=True, channel_count=2, fixed_channel_count=True)
class Balance2(UGen):
    """
    A stereo signal balancer.

    ::

        >>> left = supriya.ugens.WhiteNoise.ar()
        >>> right = supriya.ugens.SinOsc.ar()
        >>> balance_2 = supriya.ugens.Balance2.ar(
        ...     left=left,
        ...     level=1,
        ...     position=0,
        ...     right=right,
        ... )
        >>> balance_2
        <Balance2.ar()>
    """

    left = param()
    right = param()
    position = param(0.0)
    level = param(1.0)


@ugen(ar=True, kr=True, channel_count=3, fixed_channel_count=True)
class BiPanB2(UGen):
    """
    A 2D ambisonic b-format panner.

    ::

        >>> in_a = supriya.ugens.SinOsc.ar()
        >>> in_b = supriya.ugens.WhiteNoise.ar()
        >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
        ...     azimuth=-0.5,
        ...     gain=1,
        ...     in_a=in_a,
        ...     in_b=in_b,
        ... )
        >>> bi_pan_b_2
        <BiPanB2.ar()>

    ::

        >>> w, x, y = bi_pan_b_2
    """

    in_a = param()
    in_b = param()
    azimuth = param()
    gain = param(1.0)


@ugen(ar=True, kr=True, is_multichannel=True, channel_count=4)
class DecodeB2(UGen):
    """
    A 2D Ambisonic B-format decoder.

    ::

        >>> source = supriya.ugens.PinkNoise.ar()
        >>> w, x, y = supriya.ugens.PanB2.ar(
        ...     source=source,
        ...     azimuth=supriya.ugens.SinOsc.kr(),
        ... )
        >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
        ...     channel_count=4,
        ...     orientation=0.5,
        ...     w=w,
        ...     x=x,
        ...     y=y,
        ... )
        >>> decode_b_2
        <DecodeB2.ar()>
    """

    w = param()
    x = param()
    y = param()
    orientation = param(0.5)


@ugen(ar=True, kr=True, channel_count=2, fixed_channel_count=True)
class Pan2(UGen):
    """
    A two channel equal power panner.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> pan_2 = supriya.ugens.Pan2.ar(
        ...     source=source,
        ... )
        >>> pan_2
        <Pan2.ar()>
    """

    source = param()
    position = param(0.0)
    level = param(1.0)


@ugen(ar=True, kr=True, channel_count=4, fixed_channel_count=True)
class Pan4(UGen):
    """
    A four-channel equal-power panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_4 = supriya.ugens.Pan4.ar(
        ...     gain=1,
        ...     source=source,
        ...     x_position=0,
        ...     y_position=0,
        ... )
        >>> pan_4
        <Pan4.ar()>
    """

    source = param()
    x_position = param(0)
    y_position = param(0)
    gain = param(1)


@ugen(ar=True, kr=True, is_multichannel=True)
class PanAz(UGen):
    """
    A multi-channel equal-power panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_az = supriya.ugens.PanAz.ar(
        ...     channel_count=8,
        ...     amplitude=1,
        ...     orientation=0.5,
        ...     position=0,
        ...     source=source,
        ...     width=2,
        ... )
        >>> pan_az
        <PanAz.ar()>
    """

    source = param()
    position = param(0)
    amplitude = param(1)
    width = param(2)
    orientation = param(0.5)


@ugen(ar=True, kr=True, channel_count=3, fixed_channel_count=True)
class PanB(UGen):
    """
    A 3D ambisonic b-format panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_b = supriya.ugens.PanB.ar(
        ...     azimuth=0,
        ...     elevation=0,
        ...     gain=1,
        ...     source=source,
        ... )
        >>> pan_b
        <PanB.ar()>
    """

    source = param()
    azimuth = param(0)
    elevation = param(0)
    gain = param(1)


@ugen(ar=True, kr=True, channel_count=3, fixed_channel_count=True)
class PanB2(UGen):
    """
    A 2D ambisonic b-format panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_b_2 = supriya.ugens.PanB2.ar(
        ...     azimuth=0,
        ...     gain=1,
        ...     source=source,
        ... )
        >>> pan_b_2
        <PanB2.ar()>
    """

    source = param()
    azimuth = param(0)
    gain = param(1)


@ugen(ar=True, kr=True, channel_count=2, fixed_channel_count=True)
class Rotate2(UGen):
    """
    Equal-power sound-field rotator.

    ::

        >>> x = supriya.ugens.PinkNoise.ar() * 0.4
        >>> y = supriya.ugens.LFTri.ar(frequency=880)
        >>> y *= supriya.ugens.LFPulse.kr(frequency=3, width=0.1)
        >>> position = supriya.ugens.LFSaw.kr(frequency=0.1)
        >>> rotate_2 = supriya.ugens.Rotate2.ar(
        ...     x=x,
        ...     y=y,
        ...     position=position,
        ... )
        >>> rotate_2
        <Rotate2.ar()>

    Returns an array of the rotator's left and right outputs.
    """

    x = param()
    y = param()
    position = param(0)


class Splay(PseudoUGen):
    """
    A stereo signal spreader.

    ::

        >>> source = supriya.ugens.SinOsc.ar(frequency=[333, 444, 555, 666, 777])
        >>> splay = supriya.ugens.Splay.ar(source=source)
        >>> splay
        <UGenVector([<BinaryOpUGen.ar(MULTIPLICATION)[0]>, <BinaryOpUGen.ar(MULTIPLICATION)[0]>])>

    ::

        >>> print(splay)
        synthdef:
            name: ...
            ugens:
            -   SinOsc.ar/0:
                    frequency: 333.0
                    phase: 0.0
            -   Pan2.ar/0:
                    source: SinOsc.ar/0[0]
                    position: -1.0
                    level: 1.0
            -   SinOsc.ar/1:
                    frequency: 444.0
                    phase: 0.0
            -   Pan2.ar/1:
                    source: SinOsc.ar/1[0]
                    position: -0.5
                    level: 1.0
            -   SinOsc.ar/2:
                    frequency: 555.0
                    phase: 0.0
            -   Pan2.ar/2:
                    source: SinOsc.ar/2[0]
                    position: 0.0
                    level: 1.0
            -   SinOsc.ar/3:
                    frequency: 666.0
                    phase: 0.0
            -   Pan2.ar/3:
                    source: SinOsc.ar/3[0]
                    position: 0.5
                    level: 1.0
            -   Sum4.ar/0:
                    input_one: Pan2.ar/0[0]
                    input_two: Pan2.ar/1[0]
                    input_three: Pan2.ar/2[0]
                    input_four: Pan2.ar/3[0]
            -   Sum4.ar/1:
                    input_one: Pan2.ar/0[1]
                    input_two: Pan2.ar/1[1]
                    input_three: Pan2.ar/2[1]
                    input_four: Pan2.ar/3[1]
            -   SinOsc.ar/4:
                    frequency: 777.0
                    phase: 0.0
            -   Pan2.ar/4:
                    source: SinOsc.ar/4[0]
                    position: 1.0
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/0:
                    left: Sum4.ar/0[0]
                    right: Pan2.ar/4[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar/0[0]
                    right: 0.4472135954999579
            -   BinaryOpUGen(ADDITION).ar/1:
                    left: Sum4.ar/1[0]
                    right: Pan2.ar/4[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(ADDITION).ar/1[0]
                    right: 0.4472135954999579
    """

    ### CLASS VARIABLES ###

    _ordered_keys = (
        "spread",
        "level",
        "center",
        "normalize",
        "source",
    )
    _unexpanded_keys = ("source",)

    @classmethod
    def _new_expanded(cls, rate=None, **kwargs):
        def recurse(
            all_expanded_params: UGenRecursiveParams,
        ) -> UGenOperable:
            if (
                not isinstance(all_expanded_params, dict)
                and len(all_expanded_params) == 1
            ):
                all_expanded_params = all_expanded_params[0]
            if isinstance(all_expanded_params, dict):
                return cls._new_single(
                    rate=rate,
                    special_index=0,
                    **all_expanded_params,
                )
            return UGenVector(
                *(recurse(expanded_params) for expanded_params in all_expanded_params)
            )

        return Mix.multichannel(
            recurse(UGen._expand_params(kwargs, unexpanded_keys=cls._unexpanded_keys)),
            2,
        )

    @classmethod
    def _new_single(
        cls,
        *,
        rate=None,
        center=0,
        level=1,
        normalize=True,
        source=None,
        spread=1,
        **kwargs,
    ):
        positions = [
            (i * (2 / (len(source) - 1)) - 1) * spread + center
            for i in range(len(source))
        ]
        if normalize:
            if rate == CalculationRate.AUDIO:
                level = level * math.sqrt(1 / len(source))
            else:
                level = level / len(source)
        panners = _get_method_for_rate(Pan2, rate)(
            source=source, position=positions
        )
        return Mix.multichannel(panners, 2) * level

    @classmethod
    def ar(cls, *, source, center=0, level=1, normalize=True, spread=1):
        return cls._new_expanded(
            rate=CalculationRate.AUDIO,
            center=center,
            level=level,
            normalize=normalize,
            source=source,
            spread=spread,
        )

    @classmethod
    def kr(cls, *, source, center=0, level=1, normalize=True, spread=1):
        return cls._new_expanded(
            rate=CalculationRate.CONTROL,
            center=center,
            level=level,
            normalize=normalize,
            source=source,
            spread=spread,
        )


@ugen(ar=True, kr=True)
class XFade2(UGen):
    """
    Two channel equal power crossfader.

    ::

        >>> xfade_3 = supriya.ugens.XFade2.ar(
        ...     in_a=supriya.ugens.Saw.ar(),
        ...     in_b=supriya.ugens.SinOsc.ar(),
        ...     level=1,
        ...     pan=supriya.ugens.LFTri.kr(frequency=0.1),
        ... )
        >>> xfade_3
        <XFade2.ar()[0]>
    """

    in_a = param()
    in_b = param(0)
    pan = param(0)
    level = param(1)
