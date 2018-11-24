import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class LeakDC(Filter):
    """
    A DC blocker.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> leak_d_c = supriya.ugens.LeakDC.ar(
        ...     source=source,
        ...     coefficient=0.995,
        ...     )
        >>> leak_d_c
        LeakDC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('coefficient', 0.995)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
