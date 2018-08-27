import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):
    """
    Shifts phase.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> shift = supriya.ugens.LFNoise2.kr(1).scale(-1, 1, -180, 180)
        >>> pv_phase_shift = supriya.ugens.PV_PhaseShift.new(
        ...     pv_chain=pv_chain,
        ...     integrate=0,
        ...     shift=shift,
        ...     )
        >>> pv_phase_shift
        PV_PhaseShift.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([
        ('pv_chain', None),
        ('shift', None),
        ('integrate', 0),
    ])
