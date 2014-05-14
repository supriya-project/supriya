from supriya.library.audiolib.UGen import UGen
from supriya.library.audiolib import Argument


class SinOsc(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('freq', 440),
        Argument('phase', 0),
        )
