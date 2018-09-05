import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):
    """
    A bus input unit generator.

    ::

        >>> supriya.ugens.In.ar(bus=0, channel_count=4)
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _default_channel_count = 1

    _has_settable_channel_count = True

    _is_input = True

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
