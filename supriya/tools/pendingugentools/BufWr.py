# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class BufWr(UGen):
    r'''

    ::

        >>> buf_wr = ugentools.BufWr.(
        ...     buffer_id=0,
        ...     input_array=None,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> buf_wr

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'input_array',
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
        input_array=None,
        loop=1,
        phase=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        input_array=None,
        loop=1,
        phase=0,
        ):
        r'''Constructs an audio-rate BufWr.

        ::

            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_wr

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            loop=loop,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=0,
        input_array=None,
        loop=1,
        phase=0,
        ):
        r'''Constructs a control-rate BufWr.

        ::

            >>> buf_wr = ugentools.BufWr.kr(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_wr

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            loop=loop,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def input_array(self):
        r'''Gets `input_array` input of BufWr.

        ::

            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_wr.input_array

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('input_array')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufWr.

        ::

            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_wr.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of BufWr.

        ::

            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_wr.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of BufWr.

        ::

            >>> buf_wr = ugentools.BufWr.ar(
            ...     buffer_id=0,
            ...     input_array=None,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_wr.loop

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]