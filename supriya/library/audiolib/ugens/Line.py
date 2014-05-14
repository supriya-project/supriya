from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class Line(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('start', 0),
        Argument('stop', 1),
        Argument('duration', 1),
        Argument('done_action', 0),
        )
