import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Out(UGen):
    """
    A bus output unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.Out.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        Out.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0.0),
        ('source', None),
    ])

    _unexpanded_input_names = (
        'source',
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC PROPERTIES ###

    @property
    def is_output_ugen(self):
        return True
