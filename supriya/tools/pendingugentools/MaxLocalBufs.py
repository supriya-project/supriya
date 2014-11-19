# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class MaxLocalBufs(UGen):
    r'''

    ::

        >>> max_local_bufs = ugentools.MaxLocalBufs.(
        ...     )
        >>> max_local_bufs

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
        ):
        r'''Constructs a MaxLocalBufs.

        ::

            >>> max_local_bufs = ugentools.MaxLocalBufs.new(
            ...     )
            >>> max_local_bufs

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen
