import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen


class K2A(PureUGen):
    """
    A control-rate to audio-rate converter unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.kr()
        >>> k_2_a = supriya.ugens.K2A.ar(
        ...     source=source,
        ...     )
        >>> k_2_a
        K2A.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.AUDIO,)
