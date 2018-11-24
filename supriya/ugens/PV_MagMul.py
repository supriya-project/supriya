import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagMul(PV_ChainUGen):
    """
    Multiplies FFT magnitudes.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_mag_mul = supriya.ugens.PV_MagMul.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     )
        >>> pv_mag_mul
        PV_MagMul.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain_a', None), ('pv_chain_b', None)]
    )
