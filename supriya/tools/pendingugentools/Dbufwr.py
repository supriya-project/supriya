# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dbufwr(DUGen):
    r'''

    ::

        >>> dbufwr = ugentools.Dbufwr.ar(
        ...     buffer_id=0,
        ...     input=0,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> dbufwr
        Dbufwr.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'input',
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
        input=0,
        loop=1,
        phase=0,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input=input,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=0,
        input=0,
        loop=1,
        phase=0,
        ):
        r'''Constructs a Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.new(
            ...     buffer_id=0,
            ...     input=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr
            Dbufwr.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input=input,
            loop=loop,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.ar(
            ...     buffer_id=0,
            ...     input=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.buffer_id
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def input(self):
        r'''Gets `input` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.ar(
            ...     buffer_id=0,
            ...     input=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.input
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('input')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.ar(
            ...     buffer_id=0,
            ...     input=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.loop
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.ar(
            ...     buffer_id=0,
            ...     input=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr.phase
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]