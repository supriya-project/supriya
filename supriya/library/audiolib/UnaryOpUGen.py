import enum
from supriya.library.audiolib.UGen import UGen
from supriya.library.audiolib import ArgumentSpecification


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('source'),
        )

    class UnaryOperator(enum.IntEnum):
        NEG = 0
