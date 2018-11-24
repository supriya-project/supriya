import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Ringz(Filter):
    """
    A ringing filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ringz = supriya.ugens.Ringz.ar(
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ...     )
        >>> ringz
        Ringz.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('frequency', 440), ('decay_time', 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
