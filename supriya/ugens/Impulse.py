import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class Impulse(PureUGen):
    """
    A non-band-limited single-sample impulse generator unit generator.

    ::

        >>> supriya.ugens.Impulse.ar()
        Impulse.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    _ordered_input_names = collections.OrderedDict(
        [('frequency', 440.0), ('phase', 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
