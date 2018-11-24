import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class HPF(Filter):
    """
    A Highpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.HPF.ar(source=source)
        HPF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    _ordered_input_names = collections.OrderedDict(
        [('source', None), ('frequency', 440)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
