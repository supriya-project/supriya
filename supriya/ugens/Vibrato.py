import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class Vibrato(PureUGen):
    """
    Vibrato is a slow frequency modulation.

    ::

        >>> vibrato = supriya.ugens.Vibrato.ar(
        ...     delay=0,
        ...     depth=0.02,
        ...     depth_variation=0.1,
        ...     frequency=440,
        ...     initial_phase=0,
        ...     onset=0,
        ...     rate=6,
        ...     rate_variation=0.04,
        ...     )
        >>> vibrato
        Vibrato.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 440),
        ('rate', 6),
        ('depth', 0.02),
        ('delay', 0),
        ('onset', 0),
        ('rate_variation', 0.04),
        ('depth_variation', 0.1),
        ('initial_phase', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
