import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class LPZ1(Filter):
    """
    A two point average filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lpz_1 = supriya.ugens.LPZ1.ar(
        ...     source=source,
        ...     )
        >>> lpz_1
        LPZ1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict([('source', None)])

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
