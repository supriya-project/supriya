# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dgeom(DUGen):
    r'''

    ::

        >>> dgeom = ugentools.Dgeom.ar(
        ...     grow=2,
        ...     length="float('inf')",
        ...     start=1,
        ...     )
        >>> dgeom
        Dgeom.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'start',
        'grow',
        'length',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        grow=2,
        length="float('inf')",
        start=1,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            grow=grow,
            length=length,
            start=start,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        grow=2,
        length="float('inf')",
        start=1,
        ):
        r'''Constructs a Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.new(
            ...     grow=2,
            ...     length="float('inf')",
            ...     start=1,
            ...     )
            >>> dgeom
            Dgeom.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            grow=grow,
            length=length,
            start=start,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def grow(self):
        r'''Gets `grow` input of Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.ar(
            ...     grow=2,
            ...     length="float('inf')",
            ...     start=1,
            ...     )
            >>> dgeom.grow
            2.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('grow')
        return self._inputs[index]

    @property
    def length(self):
        r'''Gets `length` input of Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.ar(
            ...     grow=2,
            ...     length="float('inf')",
            ...     start=1,
            ...     )
            >>> dgeom.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def start(self):
        r'''Gets `start` input of Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.ar(
            ...     grow=2,
            ...     length="float('inf')",
            ...     start=1,
            ...     )
            >>> dgeom.start
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('start')
        return self._inputs[index]