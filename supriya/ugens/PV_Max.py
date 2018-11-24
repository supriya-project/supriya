import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_Max(PV_ChainUGen):
    """
    Maximum magnitude.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_max = supriya.ugens.PV_Max.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     )
        >>> pv_max
        PV_Max.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain_a', None), ('pv_chain_b', None)]
    )
