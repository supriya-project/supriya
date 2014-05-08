import enum
from supriya.synthdefs.UGen import UGen
from supriya.synthdefs import ArgumentSpecification


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('source'),
        )

    class UnaryOperator(enum.IntEnum):
        NEG = 0
