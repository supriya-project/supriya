import enum
from supriya.synthdefs.UGen import UGen


class UnaryOpUGen(UGen):

    class UnaryOperator(enum.IntEnum):
        NEG = 0
