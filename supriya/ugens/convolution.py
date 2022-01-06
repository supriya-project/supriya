import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Convolution(UGen):
    """
    A real-time convolver.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution = supriya.ugens.Convolution.ar(
        ...     framesize=512,
        ...     kernel=kernel,
        ...     source=source,
        ... )
        >>> convolution
        Convolution.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("kernel", None), ("framesize", 512)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Convolution2(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger
    signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_2 = supriya.ugens.Convolution2.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_2
        Convolution2.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("kernel", None), ("trigger", 0), ("framesize", 2048)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Convolution2L(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_2_l = supriya.ugens.Convolution2L.ar(
        ...     crossfade=1,
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_2_l
        Convolution2L.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("kernel", None),
            ("trigger", 0.0),
            ("framesize", 2048),
            ("crossfade", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Convolution3(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_3 = supriya.ugens.Convolution3.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_3
        Convolution3.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("kernel", None), ("trigger", 0.0), ("framesize", 2048)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)
