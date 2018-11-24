import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_CopyPhase(PV_ChainUGen):
    """
    Copies magnitudes and phases.

    ::

        >>> pv_chain_a = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = supriya.ugens.FFT(
        ...     source=supriya.ugens.LFSaw.ar(),
        ...     )
        >>> pv_copy_phase = supriya.ugens.PV_CopyPhase.new(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     )
        >>> pv_copy_phase
        PV_CopyPhase.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [('pv_chain_a', None), ('pv_chain_b', None)]
    )
