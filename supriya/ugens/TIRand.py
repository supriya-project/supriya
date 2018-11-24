import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class TIRand(UGen):
    """
    A triggered integer random number generator.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> t_i_rand = supriya.ugens.TIRand.ar(
        ...     minimum=0,
        ...     maximum=127,
        ...     trigger=trigger,
        ...     )
        >>> t_i_rand
        TIRand.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Noise UGens"

    _ordered_input_names = collections.OrderedDict(
        [("minimum", 0), ("maximum", 127), ("trigger", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, maximum=127, minimum=0, trigger=0):
        minimum = int(minimum)
        maximum = int(maximum)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            trigger=trigger,
        )
