import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class PauseSelfWhenDone(UGen):
    """
    Pauses the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
        ...     source=source,
        ...     )
        >>> pause_self_when_done
        PauseSelfWhenDone.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Envelope Utility UGens"

    _ordered_input_names = collections.OrderedDict([("source", None)])

    _valid_calculation_rates = (CalculationRate.CONTROL,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, source=None):
        if not (hasattr(source, "has_done_flag") and source.has_done_flag):
            raise ValueError(repr(source))
        UGen.__init__(self, calculation_rate=calculation_rate, source=source)
