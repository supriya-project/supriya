# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Dunique(UGen):
    r'''

    ::

        >>> dunique = ugentools.Dunique.ar(
        ...     max_buffer_size=1024,
        ...     protected=True,
        ...     source=source,
        ...     )
        >>> dunique
        Dunique.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'max_buffer_size',
        'protected',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        max_buffer_size=1024,
        protected=True,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            max_buffer_size=max_buffer_size,
            protected=protected,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        max_buffer_size=1024,
        protected=True,
        source=source,
        ):
        r'''Constructs a Dunique.

        ::

            >>> dunique = ugentools.Dunique.new(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique
            Dunique.new()

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

    ### PUBLIC PROPERTIES ###

    @property
    def max_buffer_size(self):
        r'''Gets `max_buffer_size` input of Dunique.

        ::

            >>> dunique = ugentools.Dunique.ar(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.max_buffer_size
            1024.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('max_buffer_size')
        return self._inputs[index]

    @property
    def protected(self):
        r'''Gets `protected` input of Dunique.

        ::

            >>> dunique = ugentools.Dunique.ar(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.protected
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('protected')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Dunique.

        ::

            >>> dunique = ugentools.Dunique.ar(
            ...     max_buffer_size=1024,
            ...     protected=True,
            ...     source=source,
            ...     )
            >>> dunique.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]