# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Dwhite import Dwhite


class Diwhite(Dwhite):
    r'''An integer demand-rate white noise random generator.

    ::

        >>> diwhite = ugentools.Diwhite(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     )
        >>> diwhite
        Diwhite()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'length',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        length=float('inf'),
        maximum=1,
        minimum=0,
        ):
        Dwhite.__init__(
            self,
            length=length,
            maximum=maximum,
            minimum=minimum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        length=float('inf'),
        maximum=1,
        minimum=0,
        ):
        r'''Constructs a Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite
            Diwhite()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            length=length,
            maximum=maximum,
            minimum=minimum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets `length` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.length
            inf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def maximum(self):
        r'''Gets `maximum` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.maximum
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        r'''Gets `minimum` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.minimum
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]