from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class DelayC(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        Argument('maximum_delay_time', 0.2),
        Argument('delay_time', 0.2),
        )
