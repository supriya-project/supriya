import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class TWindex(UGen):
    """
    A triggered windex.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_windex = supriya.ugens.TWindex.ar(
        ...     trigger=trigger,
        ...     normalize=0,
        ...     array=[1, 2, 3],
        ...     )
        >>> t_windex
        TWindex.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    _ordered_input_names = collections.OrderedDict([
        ('trigger', None),
        ('normalize', 0),
        ('array', None),
    ])

    _unexpanded_input_names = (
        'array',
        )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
