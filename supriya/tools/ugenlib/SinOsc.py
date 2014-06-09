from supriya.tools.synthdefinitiontools.Argument import Argument
from supriya.tools.synthdefinitiontools.UGen import UGen


class SinOsc(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('frequency', 440),
        Argument('phase', 0),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440.,
        phase=0.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )
