import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class DemandEnvGen(UGen):
    """
    A demand rate envelope generator.

    ::

        >>> demand_env_gen = supriya.ugens.DemandEnvGen.ar(
        ...     curve=0,
        ...     done_action=0,
        ...     duration=1,
        ...     gate=1,
        ...     level=1,
        ...     level_bias=0,
        ...     level_scale=1,
        ...     reset=1,
        ...     shape=1,
        ...     time_scale=1,
        ...     )
        >>> demand_env_gen
        DemandEnvGen.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ('level', None),
            ('duration', None),
            ('shape', 1),
            ('curve', 0),
            ('gate', 1),
            ('reset', 1),
            ('level_scale', 1),
            ('level_bias', 0),
            ('time_scale', 1),
            ('done_action', 0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
