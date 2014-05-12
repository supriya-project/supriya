import enum
from supriya.tools.audio.UGen import UGen
from supriya.tools.audio import ArgumentSpecification


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('source'),
        )

    class UnaryOperator(enum.IntEnum):
        NEG = 0
