import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class PanAz(MultiOutUGen):
    """
    A multi-channel equal-power panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_az = supriya.ugens.PanAz.ar(
        ...     channel_count=8,
        ...     amplitude=1,
        ...     orientation=0.5,
        ...     position=0,
        ...     source=source,
        ...     width=2,
        ...     )
        >>> pan_az
        UGenArray({8})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    _has_channel_count = 8

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('position', 0),
        ('amplitude', 1),
        ('width', 2),
        ('orientation', 0.5),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
