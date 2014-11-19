# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ListDUGen import ListDUGen


class Drand(ListDUGen):
    r'''

    ::

        >>> drand = ugentools.Drand.(
        ...     )
        >>> drand

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
        list=None,
        repeats=1,
        ):
        r'''Constructs a Drand.

        ::

            >>> drand = ugentools.Drand.new(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> drand

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            list=list,
            repeats=repeats,
            )
        return ugen
