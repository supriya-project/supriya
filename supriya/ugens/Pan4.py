import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class Pan4(MultiOutUGen):
    """
    A four-channel equal-power panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_4 = supriya.ugens.Pan4.ar(
        ...     gain=1,
        ...     source=source,
        ...     x_position=0,
        ...     y_position=0,
        ...     )
        >>> pan_4
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    _default_channel_count = 4

    _has_settable_channel_count = False

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('x_position', 0), ('y_position', 0), ('gain', 1)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
