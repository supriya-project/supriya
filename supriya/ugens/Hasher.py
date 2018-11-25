import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Hasher(UGen):
    """
    A signal hasher.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> hasher = supriya.ugens.Hasher.ar(
        ...     source=source,
        ...     )
        >>> hasher
        Hasher.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
