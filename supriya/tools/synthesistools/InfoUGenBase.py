# -*- encoding: utf-8 -*-
from supriya.tools.synthesistools.UGen import UGen


class InfoUGenBase(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        from supriya.tools import synthesistools
        ugen = cls._new(
            calculation_rate=synthesistools.CalculationRate.SCALAR,
            **kwargs
            )
        return ugen
