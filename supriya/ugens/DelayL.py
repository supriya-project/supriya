import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen


class DelayL(PureUGen):
    """
    A linear-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayL.ar(source=source)
        DelayL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Delay UGens"

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("maximum_delay_time", 0.2), ("delay_time", 0.2)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
