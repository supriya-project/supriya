import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class KeyTrack(UGen):
    """
    A key tracker.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> key_track = supriya.ugens.KeyTrack.kr(
        ...     pv_chain=pv_chain,
        ...     chroma_leak=0.5,
        ...     key_decay=2,
        ...     )
        >>> key_track
        KeyTrack.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain', None),
        ('key_decay', 2),
        ('chroma_leak', 0.5),
    ])

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
    )
