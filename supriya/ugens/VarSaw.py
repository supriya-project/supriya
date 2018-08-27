import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class VarSaw(PureUGen):
    """
    A sawtooth-triangle oscillator with variable duty.

    ::

        >>> supriya.ugens.VarSaw.ar()
        VarSaw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 440.),
        ('initial_phase', 0.),
        ('width', 0.5),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
