import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class A2K(PureUGen):
    """
    An audio-rate to control-rate convert unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> a_2_k = supriya.ugens.A2K.kr(
        ...     source=source,
        ...     )
        >>> a_2_k
        A2K.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
    ])

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
    )
