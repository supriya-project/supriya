import collections
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_JensenAndersen(PV_ChainUGen):
    """
    A FFT feature detector for onset detection.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_jensen_andersen = supriya.ugens.PV_JensenAndersen.new(
        ...     pv_chain=pv_chain,
        ...     prophfc=0.25,
        ...     prophfe=0.25,
        ...     propsc=0.25,
        ...     propsf=0.25,
        ...     threshold=1,
        ...     waittime=0.04,
        ...     )
        >>> pv_jensen_andersen
        PV_JensenAndersen.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ("pv_chain", None),
            ("propsc", 0.25),
            ("prophfe", 0.25),
            ("prophfc", 0.25),
            ("propsf", 0.25),
            ("threshold", 1),
            ("waittime", 0.04),
        ]
    )
