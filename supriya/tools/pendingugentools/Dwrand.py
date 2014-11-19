# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dwrand(DUGen):
    r'''

    ::

        >>> dwrand = ugentools.Dwrand.(
        ...     )
        >>> dwrand

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
        weights=None,
        ):
        r'''Constructs a Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.new(
            ...     list=None,
            ...     repeats=1,
            ...     weights=None,
            ...     )
            >>> dwrand

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            list=list,
            repeats=repeats,
            weights=weights,
            )
        return ugen
