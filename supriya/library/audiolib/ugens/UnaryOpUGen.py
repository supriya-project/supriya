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

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            special_index=special_index,
            )
