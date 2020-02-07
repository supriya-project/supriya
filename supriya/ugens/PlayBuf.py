import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class PlayBuf(MultiOutUGen):
    """
    A sample playback oscillator.

    ::

        >>> buffer_id = 23
        >>> play_buf = supriya.ugens.PlayBuf.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     done_action=0,
        ...     loop=0,
        ...     rate=1,
        ...     start_position=0,
        ...     trigger=1,
        ...     )
        >>> play_buf
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Buffer UGens"

    _default_channel_count = 1

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("rate", 1),
            ("trigger", 1),
            ("start_position", 0),
            ("loop", 0),
            ("done_action", 0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
