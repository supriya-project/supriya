import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_Mul(PV_ChainUGen):
    """
    Complex multiplication.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_mul = supriya.ugens.PV_Mul.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     )
        >>> pv_mul
        PV_Mul.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain_a', None),
        ('pv_chain_b', None),
    ])
