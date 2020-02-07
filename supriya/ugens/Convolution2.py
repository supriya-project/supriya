import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Convolution2(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger
    signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
        ...     supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ...     )
        >>> convolution_2 = supriya.ugens.Convolution2.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> convolution_2
        Convolution2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("kernel", None), ("trigger", 0), ("framesize", 2048)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
