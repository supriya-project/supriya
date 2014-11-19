# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dbrown(DUGen):
    r'''

    ::

        >>> dbrown = ugentools.Dbrown.(
        ...     hi=1,
        ...     length="float('inf')",
        ...     lo=0,
        ...     step=0.01,
        ...     )
        >>> dbrown

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'lo',
        'hi',
        'step',
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
        step=0.01,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            hi=hi,
            length=length,
            lo=lo,
            step=step,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        hi=1,
        length="float('inf')",
        lo=0,
        step=0.01,
        ):
        r'''Constructs a Dbrown.

        ::

            >>> dbrown = ugentools.Dbrown.new(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     step=0.01,
            ...     )
            >>> dbrown

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            hi=hi,
            length=length,
            lo=lo,
            step=step,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def hi(self):
        r'''Gets `hi` input of Dbrown.

        ::

            >>> dbrown = ugentools.Dbrown.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.hi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('hi')
        return self._inputs[index]

    @property
    def length(self):
        r'''Gets `length` input of Dbrown.

        ::

            >>> dbrown = ugentools.Dbrown.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def lo(self):
        r'''Gets `lo` input of Dbrown.

        ::

            >>> dbrown = ugentools.Dbrown.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.lo

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lo')
        return self._inputs[index]

    @property
    def step(self):
        r'''Gets `step` input of Dbrown.

        ::

            >>> dbrown = ugentools.Dbrown.ar(
            ...     hi=1,
            ...     length="float('inf')",
            ...     lo=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.step

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('step')
        return self._inputs[index]