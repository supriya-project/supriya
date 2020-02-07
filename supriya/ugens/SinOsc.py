import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen


class SinOsc(PureUGen):
    """
    A sinusoid oscillator unit generator.

    ::

        >>> supriya.ugens.SinOsc.ar()
        SinOsc.ar()

    ::

        >>> print(_)
        synthdef:
            name: ...
            ugens:
            -   SinOsc.ar:
                    frequency: 440.0
                    phase: 0.0

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Oscillator UGens"

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("phase", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
