import collections

from supriya import CalculationRate, SignalRange
from supriya.synthdefs import UGen
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


class Crackle(UGen):
    """
    A chaotic noise generator.

    ::

        >>> crackle = supriya.ugens.Crackle.ar(
        ...     chaos_parameter=1.25,
        ...     )
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
        ...    density=23,
        ...    )
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
        ...    density=23,
        ...    )
        >>> dust_2
        Dust2.ar()

    """

    _ordered_input_names = collections.OrderedDict([("density", 0.0)])
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

    __documentation_section__ = "Noise UGens"
    _ordered_input_names = collections.OrderedDict([("frequency", 500.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class PinkNoise(UGen):
    """
    A pink noise unit generator.

    ::

        >>> supriya.ugens.PinkNoise.ar()
        PinkNoise.ar()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
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
