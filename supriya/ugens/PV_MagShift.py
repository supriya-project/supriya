import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagShift(PV_ChainUGen):
    """
    Shifts and stretches magnitude bin position.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_shift = supriya.ugens.PV_MagShift.new(
        ...     pv_chain=pv_chain,
        ...     shift=0,
        ...     stretch=1,
        ...     )
        >>> pv_mag_shift
        PV_MagShift.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("pv_chain", None), ("stretch", 1), ("shift", 0)]
    )
