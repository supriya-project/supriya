import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class FOS(Filter):
    """
    A first order filter section.

    ::

        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (a2 * in(i-2)) + (b1 * out(i-1)) + (b2 * out(i-2))

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> fos = supriya.ugens.FOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     b_1=0,
        ...     source=source,
        ...     )
        >>> fos
        FOS.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('a_0', 0.0),
        ('a_1', 0.0),
        ('b_1', 0.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
