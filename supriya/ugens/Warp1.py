import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class Warp1(MultiOutUGen):
    """

    ::

        >>> warp_1 = supriya.ugens.Warp1.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     envelope_buffer_id=-1,
        ...     frequency_scaling=1,
        ...     interpolation=1,
        ...     overlaps=8,
        ...     pointer=0,
        ...     window_rand_ratio=0,
        ...     window_size=0.2,
        ...     )
        >>> warp_1
        Warp1.ar()[0]

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _default_channel_count = 1

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict(
        [
            ('buffer_id', 0),
            ('pointer', 0),
            ('frequency_scaling', 1),
            ('window_size', 0.2),
            ('envelope_buffer_id', -1),
            ('overlaps', 8),
            ('window_rand_ratio', 0),
            ('interpolation', 1),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
