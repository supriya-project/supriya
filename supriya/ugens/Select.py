import collections

from supriya.enums import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class Select(PureUGen):
    """
    A signal selector.

    ::

        >>> sources = supriya.ugens.In.ar(bus=0, channel_count=8)
        >>> selector = supriya.ugens.Phasor.kr() * 8
        >>> select = supriya.ugens.Select.ar(
        ...     sources=sources,
        ...     selector=selector,
        ...     )
        >>> select
        Select.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("selector", None), ("sources", None)]
    )

    _unexpanded_input_names = ("sources",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
