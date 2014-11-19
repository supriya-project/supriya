# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class RecordBuf(UGen):
    r'''

    ::

        >>> record_buf = ugentools.RecordBuf.(
        ...     buffer_id=0,
        ...     done_action=0,
        ...     input_array=None,
        ...     loop=1,
        ...     offset=0,
        ...     pre_level=0,
        ...     rec_level=1,
        ...     run=1,
        ...     trigger=1,
        ...     )
        >>> record_buf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'input_array',
        'buffer_id',
        'offset',
        'rec_level',
        'pre_level',
        'run',
        'loop',
        'trigger',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        done_action=0,
        input_array=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            input_array=input_array,
            loop=loop,
            offset=offset,
            pre_level=pre_level,
            rec_level=rec_level,
            run=run,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        done_action=0,
        input_array=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        r'''Constructs an audio-rate RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            input_array=input_array,
            loop=loop,
            offset=offset,
            pre_level=pre_level,
            rec_level=rec_level,
            run=run,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=0,
        done_action=0,
        input_array=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        r'''Constructs a control-rate RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.kr(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            input_array=input_array,
            loop=loop,
            offset=offset,
            pre_level=pre_level,
            rec_level=rec_level,
            run=run,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def done_action(self):
        r'''Gets `done_action` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.done_action

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def input_array(self):
        r'''Gets `input_array` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.input_array

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('input_array')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.loop

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def offset(self):
        r'''Gets `offset` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.offset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]

    @property
    def pre_level(self):
        r'''Gets `pre_level` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.pre_level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pre_level')
        return self._inputs[index]

    @property
    def rec_level(self):
        r'''Gets `rec_level` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.rec_level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rec_level')
        return self._inputs[index]

    @property
    def run(self):
        r'''Gets `run` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.run

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('run')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of RecordBuf.

        ::

            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=0,
            ...     done_action=0,
            ...     input_array=None,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]