import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class XOut(UGen):
    """
    A cross-fading bus output unit generator.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> xout = supriya.ugens.XOut.ar(
        ...     bus=0,
        ...     crossfade=0.5,
        ...     source=source,
        ...     )
        >>> xout
        XOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Input/Output UGens"

    _default_channel_count = 0

    _is_output = True

    _ordered_input_names = collections.OrderedDict(
        [("bus", 0), ("crossfade", 0), ("source", None)]
    )

    _unexpanded_input_names = ("source",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
