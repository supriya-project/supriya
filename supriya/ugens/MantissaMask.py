import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class MantissaMask(UGen):
    """
    A floating-point mantissa mask.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
        ...     source=source,
        ...     bits=3,
        ...     )
        >>> mantissa_mask
        MantissaMask.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("source", 0), ("bits", 3)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
