# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InfoUGenBase(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.SCALAR
        ugen = cls._new_expanded(
            rate=rate,
            **kwargs
            )
        return ugen
