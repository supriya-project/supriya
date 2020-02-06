import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Line(UGen):
    """
    A line generating unit generator.

    ::

        >>> supriya.ugens.Line.ar()
        Line.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Line Utility UGens"

    _has_done_flag = True

    _ordered_input_names = collections.OrderedDict(
        [("start", 0.0), ("stop", 1.0), ("duration", 1.0), ("done_action", 0.0)]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        calculation_rate=None,
        done_action=None,
        duration=None,
        stop=None,
        start=None,
    ):
        import supriya.synthdefs

        done_action = supriya.DoneAction.from_expr(int(done_action))
        return super(Line, cls)._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            stop=stop,
            start=start,
        )
