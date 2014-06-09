import enum
from supriya.tools.synthesistools.Argument import Argument
from supriya.tools.synthesistools.UGen import UGen


class BinaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('left'),
        Argument('right'),
        )

    class BinaryOperator(enum.IntEnum):
        ADD = 0
        SUB = 1
        MUL = 2
        IDIV = 3
        FDIV = 4
        MOD = 5
        EQ = 6
        NE = 7
        LT = 8
        GT = 9
        LE = 10
        GE = 11
        MIN = 12
        MAX = 13
        BIT_AND = 14
        BIT_OR = 15
        BIT_XOR = 16
        LCM = 17
        GCD = 18
        ROUND = 19
        ROUND_UP = 20
        TRUNC = 21
        ATAN2 = 22
        HYPOT = 23
        HYPOTX = 24
        POW = 25
        SHIFT_LEFT = 26
        SHIFT_RIGHT = 27
        UNSIGNED_SHIFT = 28
        FILL = 29
        RING1 = 30  # a * (b + 1) == a * b + a
        RING2 = 31  # a * b + a + b
        RING3 = 32  # a*a*b
        RING4 = 33  # a*a*b - a*b*b
        DIFFERENCE_OF_SQUARES = 34  # a*a - b*b
        SUM_OF_SQUARES = 35  # a*a + b*b
        SQUARE_OF_SUM = 36  # (a + b)^2
        SQUARE_OF_DIFFERENCE = 37  # (a - b)^2
        ABSDIFF = 38  # |a - b|
        THRESH = 39
        AMCLIP = 40
        SCALE_NEG = 41
        CLIP2 = 42
        EXCESS = 43
        FOLD2 = 44
        WRAP2 = 45
        FIRST_ARG = 46
        RANDRANGE = 47
        EXPRANDRANGE = 48

    ### INITIALIZER ###

    def __init__(
        self,
        left=None,
        right=None,
        calculation_rate=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            left=left,
            right=right,
            special_index=special_index,
            )
