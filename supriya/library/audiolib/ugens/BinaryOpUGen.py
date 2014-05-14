import enum
from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class BinaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('left'),
        Argument('right'),
        )

    class BinaryOperator(enum.IntEnum):
        PLUS = 0
        MINUS = 1
        TIMES = 2
        DIVIDE = 3
        MOD = 4
        MIN = 5
        MAX = 6
        LOG = 25
        LOG2 = 26
        LOG10 = 27
