import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class SyncSaw(PureUGen):
    """
    A sawtooth wave that is hard synched to a fundamental pitch.

    ::

        >>> sync_saw = supriya.ugens.SyncSaw.ar(
        ...     saw_frequency=440,
        ...     sync_frequency=440,
        ...     )
        >>> sync_saw
        SyncSaw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    _ordered_input_names = collections.OrderedDict(
        [("sync_frequency", 440), ("saw_frequency", 440)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
