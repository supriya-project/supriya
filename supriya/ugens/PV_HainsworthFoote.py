import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_HainsworthFoote(PV_ChainUGen):
    """
    A FFT onset detector.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_hainsworth_foote = supriya.ugens.PV_HainsworthFoote.new(
        ...     pv_chain=pv_chain,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ...     )
        >>> pv_hainsworth_foote
        PV_HainsworthFoote.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ('pv_chain', None),
            ('proph', 0),
            ('propf', 0),
            ('threshold', 1),
            ('waittime', 0.04),
        ]
    )
