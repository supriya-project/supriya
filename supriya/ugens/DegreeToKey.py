import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class DegreeToKey(PureUGen):
    """
    A signal-to-modal-pitch converter.`

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> degree_to_key = supriya.ugens.DegreeToKey.ar(
        ...     buffer_id=23,
        ...     octave=12,
        ...     source=source,
        ...     )
        >>> degree_to_key
        DegreeToKey.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    _ordered_input_names = collections.OrderedDict(
        [('buffer_id', None), ('source', None), ('octave', 12)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
