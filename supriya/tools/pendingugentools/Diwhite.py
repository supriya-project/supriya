# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Dwhite import Dwhite


class Diwhite(Dwhite):
    r'''

    ::

        >>> diwhite = ugentools.Diwhite.ar(
        ...     length="float('inf')",
        ...     maximum=1,
        ...     minimum=0,
        ...     )
        >>> diwhite
        Diwhite.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'length',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        length="float('inf')",
        maximum=1,
        minimum=0,
        ):
        Dwhite.__init__(
            self,
            calculation_rate=calculation_rate,
            length=length,
            maximum=maximum,
            minimum=minimum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        length="float('inf')",
        maximum=1,
        minimum=0,
        ):
        r'''Constructs a Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.new(
            ...     length="float('inf')",
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite
            Diwhite.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
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

            >>> diwhite = ugentools.Diwhite.ar(
            ...     length="float('inf')",
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def maximum(self):
        r'''Gets `maximum` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.ar(
            ...     length="float('inf')",
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

            >>> diwhite = ugentools.Diwhite.ar(
            ...     length="float('inf')",
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.minimum
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]