import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class SOS(Filter):
    """
    A second-order filter section.

    ::

        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (b1 * out(i-1))

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> sos = supriya.ugens.SOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     a_2=0,
        ...     b_1=0,
        ...     b_2=0,
        ...     source=source,
        ...     )
        >>> sos
        SOS.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('a_0', 0), ('a_1', 0), ('a_2', 0), ('b_1', 0), ('b_2', 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
