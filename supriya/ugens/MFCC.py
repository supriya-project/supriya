import collections
from supriya import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class MFCC(MultiOutUGen):
    """
    Mel frequency cepstral coefficients.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> mfcc = supriya.ugens.MFCC.kr(
        ...     pv_chain=pv_chain,
        ...     channel_count=13,
        ...     )
        >>> mfcc
        UGenArray({13})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    _has_channel_count = True

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain', None),
    ])

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
    )
