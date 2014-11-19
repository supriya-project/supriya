# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ListDUGen import ListDUGen


class Dseq(ListDUGen):
    r'''

    ::

        >>> dseq = ugentools.Dseq.(
        ...     )
        >>> dseq

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
        r'''Constructs a Dseq.

        ::

            >>> dseq = ugentools.Dseq.new(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dseq

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
