from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class Dust(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('density', 0.),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def signal_range(self):
        return self.SignalRange.UNIPOLAR
