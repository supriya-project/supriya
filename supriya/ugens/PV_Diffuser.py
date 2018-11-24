import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_Diffuser(PV_ChainUGen):
    """
    Shifts phases randomly.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_diffuser = supriya.ugens.PV_Diffuser.new(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     )
        >>> pv_diffuser
        PV_Diffuser.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("pv_chain", None), ("trigger", 0)])
