# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dreset(DUGen):
    r'''

    ::

        >>> dreset = ugentools.Dreset.(
        ...     )
        >>> dreset

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
        reset=0,
        source=None,
        ):
        r'''Constructs a Dreset.

        ::

            >>> dreset = ugentools.Dreset.new(
            ...     reset=0,
            ...     source=None,
            ...     )
            >>> dreset

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            source=source,
            )
        return ugen
