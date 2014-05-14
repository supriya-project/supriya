from supriya.library.audiolib.UGen import UGen
from supriya.library.audiolib import Argument


class Line(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('start', 0),
        Argument('end', 1),
        Argument('dur', 1),
        Argument('doneAction', 0),
        )
