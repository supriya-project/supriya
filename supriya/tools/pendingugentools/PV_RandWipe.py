# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RandWipe(PV_ChainUGen):
    r'''

    ::

        >>> pv_rand_wipe = ugentools.PV_RandWipe.(
        ...     )
        >>> pv_rand_wipe

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
        buffer_a=None,
        buffer_b=None,
        trigger=0,
        wipe=0,
        ):
        r'''Constructs a PV_RandWipe.

        ::

            >>> pv_rand_wipe = ugentools.PV_RandWipe.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen
