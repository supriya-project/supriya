# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Dunique(UGen):
    r'''

    ::

        >>> dunique = ugentools.Dunique.(
        ...     )
        >>> dunique

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
        max_buffer_size=1024,
        protected=True,
        source=None,
        ):
        r'''Constructs a Dunique.

        ::

            >>> dunique = ugentools.Dunique.new(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=None,
            ...     )
            >>> dunique

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            max_buffer_size=max_buffer_size,
            protected=protected,
            source=source,
            )
        return ugen
