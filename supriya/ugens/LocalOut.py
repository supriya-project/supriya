import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LocalOut(UGen):
    """
    A SynthDef-local bus output.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.LocalOut.ar(
        ...     source=source,
        ...     )
        LocalOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _ordered_input_names = collections.OrderedDict([('source', None)])

    _unexpanded_input_names = ('source',)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
