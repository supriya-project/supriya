import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class RLPF(Filter):
    """
    A resonant lowpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.RLPF.ar(source=source)
        RLPF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440), ("reciprocal_of_q", 1.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
