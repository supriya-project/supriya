import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class Saw(PureUGen):
    """
    A band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.Saw.ar()
        Saw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    _ordered_input_names = collections.OrderedDict([
        ('frequency', 440.),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
