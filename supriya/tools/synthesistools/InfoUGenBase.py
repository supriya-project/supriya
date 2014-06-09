from supriya.tools.synthesistools.UGen import UGen


class InfoUGenBase(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        ugen = cls._new(
            calculation_rate=CalculationRate.SCALAR,
            **kwargs
            )
        return ugen
