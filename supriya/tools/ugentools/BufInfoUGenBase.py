from supriya.tools.synthdefinitiontools.Argument import Argument
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


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
        from supriya.tools import synthdefinitiontools
        ugen = cls._new(
            calculation_rate=synthdefinitiontools.CalculationRate.SCALAR,
            buffer_number=buffer_number,
            )
        return ugen

    @classmethod
    def kr(cls, buffer_number=None):
        from supriya.tools import synthdefinitiontools
        ugen = cls._new(
            calculation_rate=synthdefinitiontools.CalculationRate.CONTROL,
            buffer_number=buffer_number,
            )
        return ugen
