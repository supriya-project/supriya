from supriya.library.audiolib import Argument
from supriya.library.audiolib.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('bus', 0),
        )
