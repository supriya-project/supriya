# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InfoUGenBase(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            **kwargs
            )
        return ugen
