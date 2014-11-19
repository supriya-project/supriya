# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dwhite(DUGen):
    r'''

    ::

        >>> dwhite = ugentools.Dwhite.(
        ...     )
        >>> dwhite

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
        hi=1,
        length="float('inf')",
        lo=0,
        ):
        r'''Constructs a Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.new(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> dwhite

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            hi=hi,
            length=length,
            lo=lo,
            )
        return ugen
