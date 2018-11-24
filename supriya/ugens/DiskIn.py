import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class DiskIn(MultiOutUGen):
    """
    Streams in audio from a file.

    ::

        >>> buffer_id = 23
        >>> disk_in = supriya.ugens.DiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ...     )
        >>> disk_in
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _default_channel_count = 1

    _has_done_flag = True

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict([("buffer_id", None), ("loop", 0.0)])

    _valid_calculation_rates = (CalculationRate.AUDIO,)
