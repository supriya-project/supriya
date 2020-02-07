import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class PitchShift(UGen):
    """
    A pitch shift unit generator.

    ::

        >>> source = supriya.ugens.SoundIn.ar()
        >>> supriya.ugens.PitchShift.ar(
        ...     source=source,
        ...     )
        PitchShift.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Pitchshift UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("window_size", 0.2),
            ("pitch_ratio", 1.0),
            ("pitch_dispersion", 0.0),
            ("time_dispersion", 0.0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
