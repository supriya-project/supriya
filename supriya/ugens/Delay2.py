import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class Delay2(PureUGen):
    """
    A two-sample delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay2.ar(source=source)
        Delay2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('maximum_delay_time', 0.2), ('delay_time', 0.2)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
