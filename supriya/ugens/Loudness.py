import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Loudness(UGen):
    """
    Extraction of instantaneous loudness in `sones`.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> loudness = supriya.ugens.Loudness.kr(
        ...     pv_chain=pv_chain,
        ...     smask=0.25,
        ...     tmask=1,
        ...     )
        >>> loudness
        Loudness.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain', None),
        ('smask', 0.25),
        ('tmask', 1),
    ])

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
    )
