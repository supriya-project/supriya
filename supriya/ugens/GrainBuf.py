import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class GrainBuf(MultiOutUGen):
    """

    ::

        >>> grain_buf = supriya.ugens.GrainBuf.ar(
        ...     channel_count=2,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     interpolate=2,
        ...     maximum_overlap=512,
        ...     pan=0,
        ...     position=0,
        ...     rate=1,
        ...     buffer_id=0,
        ...     trigger=0,
        ...     )
        >>> grain_buf
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _has_channel_count = True

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict([
        ('trigger', 0),
        ('duration', 1),
        ('buffer_id', None),
        ('rate', 1),
        ('position', 0),
        ('interpolate', 2),
        ('pan', 0),
        ('envelope_buffer_id', -1),
        ('maximum_overlap', 512),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
    )
