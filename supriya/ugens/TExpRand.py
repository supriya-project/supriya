import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class TExpRand(UGen):
    """
    A triggered exponential random number generator.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_exp_rand = supriya.ugens.TExpRand.ar(
        ...     minimum=-1.,
        ...     maximum=1.,
        ...     trigger=trigger,
        ...     )
        >>> t_exp_rand
        TExpRand.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    _ordered_input_names = collections.OrderedDict(
        [('minimum', 0.01), ('maximum', 1), ('trigger', 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
