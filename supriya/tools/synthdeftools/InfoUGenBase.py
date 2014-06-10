# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InfoUGenBase(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        from supriya.tools import synthdeftools
        ugen = cls._new(
            calculation_rate=synthdeftools.CalculationRate.SCALAR,
            **kwargs
            )
        return ugen
