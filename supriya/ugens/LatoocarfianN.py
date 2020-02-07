import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class LatoocarfianN(UGen):
    """
    A non-interpolating Latoocarfian chaotic generator.

    ::

        >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ...     )
        >>> latoocarfian_n
        LatoocarfianN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Chaos UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 22050),
            ("a", 1),
            ("b", 3),
            ("c", 0.5),
            ("d", 0.5),
            ("xi", 0.5),
            ("yi", 0.5),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO,)
