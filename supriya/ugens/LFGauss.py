import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class LFGauss(UGen):
    """
    A non-band-limited gaussian function oscillator.

    ::

        >>> supriya.ugens.LFGauss.ar()
        LFGauss.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Oscillator UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("duration", 1),
            ("width", 0.1),
            ("initial_phase", 0),
            ("loop", 1),
            ("done_action", 0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        duration=1,
        initial_phase=0,
        loop=1,
        width=0.1,
    ):
        import supriya.synthdefs

        done_action = supriya.synthdefs.DoneAction.from_expr(done_action)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            initial_phase=initial_phase,
            loop=loop,
            width=width,
        )
