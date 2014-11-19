# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Dwhite import Dwhite


class Diwhite(Dwhite):
    r'''

    ::

        >>> diwhite = ugentools.Diwhite.(
        ...     hi=1,
        ...     length="float('inf')",
        ...     lo=0,
        ...     )
        >>> diwhite

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
        Dwhite.__init__(
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
        r'''Constructs a Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.new(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> diwhite

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
        r'''Gets `hi` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> diwhite.hi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('hi')
        return self._inputs[index]

    @property
    def length(self):
        r'''Gets `length` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> diwhite.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def lo(self):
        r'''Gets `lo` input of Diwhite.

        ::

            >>> diwhite = ugentools.Diwhite.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     )
            >>> diwhite.lo

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lo')
        return self._inputs[index]