# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class ListDUGen(DUGen):
    r'''

    ::

        >>> list_dugen = ugentools.ListDUGen.(
        ...     )
        >>> list_dugen

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
        r'''Constructs a ListDUGen.

        ::

            >>> list_dugen = ugentools.ListDUGen.new(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> list_dugen

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
