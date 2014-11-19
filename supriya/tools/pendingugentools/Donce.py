# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Donce(DUGen):
    r'''

    ::

        >>> donce = ugentools.Donce.(
        ...     )
        >>> donce

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
        source=None,
        ):
        r'''Constructs a Donce.

        ::

            >>> donce = ugentools.Donce.new(
            ...     source=None,
            ...     )
            >>> donce

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen
