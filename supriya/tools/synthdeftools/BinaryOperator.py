# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class BinaryOperator(Enumeration):

    ### CLASS VARIABLES ###

    ABSDIFF = 38  # |a - b|
    ADD = 0
    AMCLIP = 40
    ATAN2 = 22
    BIT_AND = 14
    BIT_OR = 15
    BIT_XOR = 16
    CLIP2 = 42
    DIFFERENCE_OF_SQUARES = 34  # a*a - b*b
    EQ = 6
    EXCESS = 43
    EXPRANDRANGE = 48
    FDIV = 4
    FILL = 29
    FIRST_ARG = 46
    FOLD2 = 44
    GCD = 18
    GE = 11
    GT = 9
    HYPOT = 23
    HYPOTX = 24
    IDIV = 3
    LCM = 17
    LE = 10
    LT = 8
    MAX = 13
    MIN = 12
    MOD = 5
    MUL = 2
    NE = 7
    POW = 25
    RANDRANGE = 47
    RING1 = 30  # a * (b + 1) == a * b + a
    RING2 = 31  # a * b + a + b
    RING3 = 32  # a*a*b
    RING4 = 33  # a*a*b - a*b*b
    ROUND = 19
    ROUND_UP = 20
    SCALE_NEG = 41
    SHIFT_LEFT = 26
    SHIFT_RIGHT = 27
    SQUARE_OF_DIFFERENCE = 37  # (a - b)^2
    SQUARE_OF_SUM = 36  # (a + b)^2
    SUB = 1
    SUM_OF_SQUARES = 35  # a*a + b*b
    THRESH = 39
    TRUNC = 21
    UNSIGNED_SHIFT = 28
    WRAP2 = 45
