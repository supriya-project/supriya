import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class FreeSelf(UGen):
    """
    Frees the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free_self = supriya.ugens.FreeSelf.kr(
        ...     trigger=trigger,
        ...     )
        >>> free_self
        FreeSelf.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    _ordered_input_names = collections.OrderedDict([('trigger', None)])

    _valid_calculation_rates = (CalculationRate.CONTROL,)
