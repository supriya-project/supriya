import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class FSinOsc(UGen):
    """
    Very fast sine wave generator (2 PowerPC instructions per output sample!)
    implemented using a ringing filter.

    ::

        >>> fsin_osc = supriya.ugens.FSinOsc.ar(
        ...     frequency=440,
        ...     initial_phase=0,
        ...     )
        >>> fsin_osc
        FSinOsc.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 440.0),
        ('initial_phase', 0.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
