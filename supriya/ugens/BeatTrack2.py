import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class BeatTrack2(MultiOutUGen):
    """
    A template-matching beat-tracker.

    ::

        >>> beat_track_2 = supriya.ugens.BeatTrack2.kr(
        ...     bus_index=0,
        ...     lock=False,
        ...     feature_count=4,
        ...     phase_accuracy=0.02,
        ...     weighting_scheme=-2.1,
        ...     window_size=2,
        ...     )
        >>> beat_track_2
        UGenArray({6})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Machine Listening UGens"

    _default_channel_count = 6

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [
            ("bus_index", 0.0),
            ("feature_count", None),
            ("window_size", 2),
            ("phase_accuracy", 0.02),
            ("lock", 0.0),
            ("weighting_scheme", -2.1),
        ]
    )

    _valid_calculation_rates = (CalculationRate.CONTROL,)
