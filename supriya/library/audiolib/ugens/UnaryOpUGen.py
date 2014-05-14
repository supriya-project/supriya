import enum
from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        )

    class UnaryOperator(enum.IntEnum):
        NEG = 0
