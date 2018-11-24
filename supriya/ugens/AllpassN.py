import collections

from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class AllpassN(PureUGen):
    """
    A non-interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_n = supriya.ugens.AllpassN.ar(source=source)
        >>> allpass_n
        AllpassN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Delay UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
