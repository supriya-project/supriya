# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InfoUGenBase(UGen):
    r'''Abstract base class for scalar-rate information ugens.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        r'''Constructs a scalar-rate information ugen.

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.SCALAR
        ugen = cls._new_expanded(
            rate=rate,
            **kwargs
            )
        return ugen