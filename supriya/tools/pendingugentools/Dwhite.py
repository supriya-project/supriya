# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dwhite(DUGen):
    r'''

    ::

        >>> dwhite = ugentools.Dwhite.(
        ...     hi=1,
        ...     length="float('inf')",
        ...     lo=0,
        ...     )
        >>> dwhite

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'lo',
        'hi',
        'length',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        hi=1,
        length="float('inf')",
        lo=0,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            hi=hi,
            length=length,
            lo=lo,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        hi=1,
        length="float('inf')",
        lo=0,
        ):
        r'''Constructs a Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.new(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> dwhite

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            hi=hi,
            length=length,
            lo=lo,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def hi(self):
        r'''Gets `hi` input of Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> dwhite.hi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('hi')
        return self._inputs[index]

    @property
    def length(self):
        r'''Gets `length` input of Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> dwhite.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def lo(self):
        r'''Gets `lo` input of Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> dwhite.lo

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lo')
        return self._inputs[index]