import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class DelTapRd(UGen):
    """
    A delay tap reader unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.SoundIn.ar(0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )

    ::

        >>> tapin
        DelTapWr.ar()

    ::

        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ...     )

    ::

        >>> tapout
        DelTapRd.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    _ordered_input_names = collections.OrderedDict([
        ('buffer_id', None),
        ('phase', None),
        ('delay_time', 0.0),
        ('interpolation', 1.0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
