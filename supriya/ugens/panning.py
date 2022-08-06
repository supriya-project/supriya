import collections
import math

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, PseudoUGen, UGen
from supriya.ugens.basic import Mix


class Balance2(MultiOutUGen):
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
        UGenArray({2})

    """

    _default_channel_count = 2
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("left", None), ("right", None), ("position", 0.0), ("level", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BiPanB2(MultiOutUGen):
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
        UGenArray({3})

    ::

        >>> w, x, y = bi_pan_b_2

    """

    _default_channel_count = 3
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("in_a", None), ("in_b", None), ("azimuth", None), ("gain", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DecodeB2(MultiOutUGen):
    """
    A 2D Ambisonic B-format decoder.

    ::

        >>> source = supriya.ugens.PinkNoise.ar()
        >>> w, x, y = supriya.ugens.PanB2.ar(
        ...     source=source,
        ...     azimuth=supriya.ugens.SinOsc.kr(),
        ... )
        >>> channel_count = 4
        >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
        ...     channel_count=channel_count,
        ...     orientation=0.5,
        ...     w=w,
        ...     x=x,
        ...     y=y,
        ... )
        >>> decode_b_2
        UGenArray({4})

    """

    _default_channel_count = 4
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [("w", None), ("x", None), ("y", None), ("orientation", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Pan2(MultiOutUGen):
    """
    A two channel equal power panner.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> pan_2 = supriya.ugens.Pan2.ar(
        ...     source=source,
        ... )
        >>> pan_2
        UGenArray({2})

    """

    _default_channel_count = 2
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("position", 0.0), ("level", 1.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Pan4(MultiOutUGen):
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
        UGenArray({4})

    """

    _default_channel_count = 4
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("x_position", 0), ("y_position", 0), ("gain", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class PanAz(MultiOutUGen):
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
        UGenArray({8})

    """

    _default_channel_count = 1
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("position", 0),
            ("amplitude", 1),
            ("width", 2),
            ("orientation", 0.5),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class PanB(MultiOutUGen):
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
        UGenArray({3})

    """

    _default_channel_count = 3
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("azimuth", 0), ("elevation", 0), ("gain", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class PanB2(MultiOutUGen):
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
        UGenArray({3})

    """

    _default_channel_count = 3
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("azimuth", 0), ("gain", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Rotate2(MultiOutUGen):
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
        UGenArray({2})

    Returns an array of the rotator's left and right outputs.
    """

    _default_channel_count = 2
    _has_settable_channel_count = False
    _ordered_input_names = collections.OrderedDict(
        [("x", None), ("y", None), ("position", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Splay(PseudoUGen):
    """
    A stereo signal spreader.

    ::

        >>> source = supriya.ugens.SinOsc.ar(frequency=[333, 444, 555, 666, 777])
        >>> splay = supriya.ugens.Splay.ar(source=source)
        >>> splay
        UGenArray({2})

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

    _ordered_input_names = collections.OrderedDict(
        [
            ("spread", 1),
            ("level", 1),
            ("center", 0),
            ("normalize", True),
            ("source", None),
        ]
    )
    _unexpanded_input_names = ("source",)

    @classmethod
    def _new_expanded(cls, calculation_rate=None, **kwargs):
        dictionaries = UGen._expand_dictionary(
            kwargs, unexpanded_input_names=["source"]
        )
        ugens = [
            cls._new_single(calculation_rate=calculation_rate, **dictionary)
            for dictionary in dictionaries
        ]
        return Mix.multichannel(ugens, 2)

    ### CLASS METHODS ###

    @classmethod
    def _new_single(
        cls,
        calculation_rate=None,
        center=0,
        level=1,
        normalize=True,
        source=None,
        spread=1,
    ):
        positions = [
            (i * (2 / (len(source) - 1)) - 1) * spread + center
            for i in range(len(source))
        ]
        if normalize:
            if calculation_rate == CalculationRate.AUDIO:
                level = level * math.sqrt(1 / len(source))
            else:
                level = level / len(source)
        panners = UGen._get_method_for_rate(Pan2, calculation_rate)(
            source=source, position=positions
        )
        return Mix.multichannel(panners, 2) * level

    @classmethod
    def ar(cls, *, center=0, level=1, normalize=True, source=None, spread=1):
        return cls._new_expanded(
            calculation_rate=CalculationRate.AUDIO,
            center=center,
            level=level,
            normalize=normalize,
            source=source,
            spread=spread,
        )

    @classmethod
    def kr(cls, *, center=0, level=1, normalize=True, source=None, spread=1):
        return cls._new_expanded(
            calculation_rate=CalculationRate.CONTROL,
            center=center,
            level=level,
            normalize=normalize,
            source=source,
            spread=spread,
        )


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
        XFade2.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("in_a", None), ("in_b", 0), ("pan", 0), ("level", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
