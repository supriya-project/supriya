from supriya.library.audiolib.Argument import Argument
from supriya.library.ugenlib.InfoUGenBase import InfoUGenBase


class BufInfoUGenBase(InfoUGenBase):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('buffer_number'),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_number=None,
        calculation_rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            buffer_number=buffer_number,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, buffer_number=None):
        from supriya.library import audiolib
        ugen = cls._new(
            calculation_rate=audiolib.CalculationRate.SCALAR,
            buffer_number=buffer_number,
            )
        return ugen

    @classmethod
    def kr(cls, buffer_number=None):
        from supriya.library import audiolib
        ugen = cls._new(
            calculation_rate=audiolib.CalculationRate.CONTROL,
            buffer_number=buffer_number,
            )
        return ugen
