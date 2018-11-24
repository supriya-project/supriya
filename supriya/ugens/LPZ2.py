import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class LPZ2(Filter):
    """
    A two zero fixed lowpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lpz_2 = supriya.ugens.LPZ2.ar(
        ...     source=source,
        ...     )
        >>> lpz_2
        LPZ2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict([('source', None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
