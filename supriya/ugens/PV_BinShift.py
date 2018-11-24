import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_BinShift(PV_ChainUGen):
    """
    Shifts and stretches bin positions.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_bin_shift = supriya.ugens.PV_BinShift.new(
        ...     pv_chain=pv_chain,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ...     )
        >>> pv_bin_shift
        PV_BinShift.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain', None), ('stretch', 1), ('shift', 0), ('interpolate', 0)]
    )
