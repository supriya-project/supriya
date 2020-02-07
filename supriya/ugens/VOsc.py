import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen


class VOsc(PureUGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc = supriya.ugens.VOsc.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
        ...     frequency=440,
        ...     phase=0,
        ...     )
        >>> vosc
        VOsc.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("frequency", 440), ("phase", 0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
