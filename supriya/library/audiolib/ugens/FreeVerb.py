from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class FreeVerb(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        Argument('mix', 0.33),
        Argument('room_size', 0.5),
        Argument('damping', 0.5),
        )
