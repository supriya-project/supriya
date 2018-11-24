import collections
from uqbar.enums import IntEnumeration
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Onsets(UGen):
    """
    An onset detector.

    ::

        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> pv_chain = supriya.ugens.FFT(source=source)
        >>> onsets = supriya.ugens.Onsets.kr(
        ...     pv_chain=pv_chain,
        ...     floor=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype=supriya.ugens.Onsets.ODFType.RCOMPLEX,
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ...     )
        >>> onsets
        Onsets.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    _ordered_input_names = collections.OrderedDict(
        [
            ('pv_chain', None),
            ('threshold', 0.5),
            ('odftype', 3),
            ('relaxtime', 1),
            ('floor', 0.1),
            ('mingap', 10),
            ('medianspan', 11),
            ('whtype', 1),
            ('rawodf', 0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.CONTROL,)

    class ODFType(IntEnumeration):
        POWER = 0
        MAGSUM = 1
        COMPLEX = 2
        RCOMPLEX = 3
        PHASE = 4
        WPHASE = 5
        MKL = 6
