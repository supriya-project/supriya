import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_BrickWall(PV_ChainUGen):
    """
    Zeros bins.

    - If wipe == 0 then there is no effect.
    - If wipe > 0 then it acts like a high pass filter, clearing bins from the
      bottom up.
    - If wipe < 0 then it acts like a low pass filter, clearing bins from the
      top down.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_brick_wall = supriya.ugens.PV_BrickWall.new(
        ...     pv_chain=pv_chain,
        ...     wipe=0,
        ...     )
        >>> pv_brick_wall
        PV_BrickWall.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([('pv_chain', None), ('wipe', 0)])
