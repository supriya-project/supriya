import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen


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
        ...     )
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
        ...     )
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
        ...     )
        >>> channel_count = 4
        >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
        ...     channel_count=channel_count,
        ...     orientation=0.5,
        ...     w=w,
        ...     x=x,
        ...     y=y,
        ...     )
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
        ...     )
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
        ...     )
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
        ...     )
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
        ...     )
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
        ...     )
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
        ...     )
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


class XFade2(UGen):
    """
    Two channel equal power crossfader.

    ::

        >>> xfade_3 = supriya.ugens.XFade2.ar(
        ...     in_a=supriya.ugens.Saw.ar(),
        ...     in_b=supriya.ugens.SinOsc.ar(),
        ...     level=1,
        ...     pan=supriya.ugens.LFTri.kr(frequency=0.1),
        ...     )
        >>> xfade_3
        XFade2.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("in_a", None), ("in_b", 0), ("pan", 0), ("level", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
