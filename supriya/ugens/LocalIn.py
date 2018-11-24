import collections

from supriya import utils
from supriya.enums import CalculationRate
from supriya.ugens.MultiOutUGen import MultiOutUGen


class LocalIn(MultiOutUGen):
    """
    A SynthDef-local bus input.

    ::

        >>> supriya.ugens.LocalIn.ar(channel_count=2)
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Input/Output UGens"

    _default_channel_count = 1

    _has_settable_channel_count = True

    _ordered_input_names = collections.OrderedDict([("default", 0)])

    _unexpanded_input_names = ("default",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, channel_count=1, default=0):
        if not isinstance(default, collections.Sequence):
            default = (default,)
        default = (float(_) for _ in default)
        default = utils.repeat_sequence_to_length(default, channel_count)
        default = list(default)[:channel_count]
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
        )
