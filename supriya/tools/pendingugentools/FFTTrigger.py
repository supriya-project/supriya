# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class FFTTrigger(PV_ChainUGen):
    r'''

    ::

        >>> ffttrigger = ugentools.FFTTrigger.(
        ...     )
        >>> ffttrigger

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_=None,
        hop=0.5,
        polar=0,
        ):
        r'''Constructs a FFTTrigger.

        ::

            >>> ffttrigger = ugentools.FFTTrigger.new(
            ...     buffer_=None,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            hop=hop,
            polar=polar,
            )
        return ugen
