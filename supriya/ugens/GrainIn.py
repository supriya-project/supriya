import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen


class GrainIn(MultiOutUGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> grain_in = supriya.ugens.GrainIn.ar(
        ...     channel_count=2,
        ...     duration=1,
        ...     envelope_buffer_id=-1,
        ...     maximum_overlap=512,
        ...     position=0,
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> grain_in
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _default_channel_count = 1

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict(
        [
            ("trigger", 0),
            ("duration", 1),
            ("source", None),
            ("position", 0),
            ("envelope_buffer_id", -1),
            ("maximum_overlap", 512),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
