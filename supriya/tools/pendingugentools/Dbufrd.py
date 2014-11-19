# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dbufrd(DUGen):
    r'''

    ::

        >>> dbufrd = ugentools.Dbufrd.(
        ...     buffer_id=0,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> dbufrd

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'loop',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        loop=1,
        phase=0,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=0,
        loop=1,
        phase=0,
        ):
        r'''Constructs a Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd.new(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            loop=loop,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd.ar(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd.ar(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd.loop

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd.ar(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]