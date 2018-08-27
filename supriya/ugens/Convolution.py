import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Convolution(UGen):
    """
    A real-time convolver.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
        ...     supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ...     )
        >>> convolution = supriya.ugens.Convolution.ar(
        ...     framesize=512,
        ...     kernel=kernel,
        ...     source=source,
        ...     )
        >>> convolution
        Convolution.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('kernel', None),
        ('framesize', 512),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
