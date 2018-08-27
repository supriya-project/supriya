import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagDiv(PV_ChainUGen):
    """
    Divides magnitudes.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_mag_div = supriya.ugens.PV_MagDiv.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     zeroed=0.0001,
        ...     )
        >>> pv_mag_div
        PV_MagDiv.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain_a', None),
        ('pv_chain_b', None),
        ('zeroed', 0.0001),
    ])
