import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class BPF(Filter):
    """
    A 2nd order Butterworth bandpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> b_p_f = supriya.ugens.BPF.ar(source=source)
        >>> b_p_f
        BPF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Filter UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 440.0), ("reciprocal_of_q", 1.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
