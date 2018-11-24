import collections

from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class COsc(PureUGen):
    """
    A chorusing wavetable oscillator.

    ::

        >>> cosc = supriya.ugens.COsc.ar(
        ...     beats=0.5,
        ...     buffer_id=23,
        ...     frequency=440,
        ...     )
        >>> cosc
        COsc.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Oscillator UGens"

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("frequency", 440.0), ("beats", 0.5)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
