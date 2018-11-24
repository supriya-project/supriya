import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class BufRd(MultiOutUGen):
    """
    A buffer-reading oscillator.

    ::

        >>> buffer_id = 23
        >>> phase = supriya.ugens.Phasor.ar(
        ...     rate=supriya.ugens.BufRateScale.kr(buffer_id),
        ...     start=0,
        ...     stop=supriya.ugens.BufFrames.kr(buffer_id),
        ...     )
        >>> buf_rd = supriya.ugens.BufRd.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     interpolation=2,
        ...     loop=1,
        ...     phase=phase,
        ...     )
        >>> buf_rd
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    _default_channel_count = 1

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict(
        [('buffer_id', None), ('phase', 0.0), ('loop', 1.0), ('interpolation', 2.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
