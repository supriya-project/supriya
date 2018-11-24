import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_ConformalMap(PV_ChainUGen):
    """
    Complex plane attack.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_conformal_map = supriya.ugens.PV_ConformalMap.new(
        ...     aimag=0,
        ...     areal=0,
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_conformal_map
        PV_ConformalMap.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain', None), ('areal', 0), ('aimag', 0)]
    )
