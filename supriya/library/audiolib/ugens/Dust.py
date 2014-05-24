from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class Dust(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('density', 0.),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        density=0.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            density=density,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def signal_range(self):
        return self.SignalRange.UNIPOLAR
