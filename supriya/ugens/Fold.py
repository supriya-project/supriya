import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Fold(UGen):
    """
    Folds a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> fold = supriya.ugens.Fold.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> fold
        Fold.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('minimum', 0.0),
        ('maximum', 1.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        CalculationRate.SCALAR,
    )
