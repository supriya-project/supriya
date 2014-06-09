from supriya.tools.synthesistools.Argument import Argument
from supriya.tools.synthesistools.InfoUGenBase import InfoUGenBase


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
        from supriya.tools import synthesistools
        ugen = cls._new(
            calculation_rate=synthesistools.CalculationRate.SCALAR,
            buffer_number=buffer_number,
            )
        return ugen

    @classmethod
    def kr(cls, buffer_number=None):
        from supriya.tools import synthesistools
        ugen = cls._new(
            calculation_rate=synthesistools.CalculationRate.CONTROL,
            buffer_number=buffer_number,
            )
        return ugen
