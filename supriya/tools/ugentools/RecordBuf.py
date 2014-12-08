# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class RecordBuf(UGen):
    r'''Records or overdubs into a buffer.

    ::

        >>> buffer_id = 23
        >>> source = ugentools.SoundIn.ar(bus=(0, 1))
        >>> record_buf = ugentools.RecordBuf.ar(
        ...     buffer_id=buffer_id,
        ...     done_action=0,
        ...     source=source,
        ...     loop=1,
        ...     offset=0,
        ...     pre_level=0,
        ...     rec_level=1,
        ...     run=1,
        ...     trigger=1,
        ...     )
        >>> record_buf
        RecordBuf.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'offset',
        'rec_level',
        'pre_level',
        'run',
        'loop',
        'trigger',
        'done_action',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        done_action=0,
        source=None,
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
            source=source,
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
        buffer_id=None,
        done_action=0,
        source=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        r'''Constructs an audio-rate RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf
            RecordBuf.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            source=source,
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
        buffer_id=None,
        done_action=0,
        source=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        r'''Constructs a control-rate RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.kr(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf
            RecordBuf.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            done_action=done_action,
            source=source,
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

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.buffer_id
            23.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def done_action(self):
        r'''Gets `done_action` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.done_action
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        r'''Is true if UGen has a done flag.

        Returns boolean.
        '''
        return True

    @property
    def source(self):
        r'''Gets `source` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.source
            OutputProxy(
                source=In(
                    bus=OutputProxy(
                        source=NumOutputBuses(
                            calculation_rate=<CalculationRate.SCALAR: 0>
                            ),
                        output_index=0
                        ),
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=2
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.loop
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def offset(self):
        r'''Gets `offset` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.offset
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]

    @property
    def pre_level(self):
        r'''Gets `pre_level` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.pre_level
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pre_level')
        return self._inputs[index]

    @property
    def rec_level(self):
        r'''Gets `rec_level` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.rec_level
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rec_level')
        return self._inputs[index]

    @property
    def run(self):
        r'''Gets `run` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.run
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('run')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of RecordBuf.

        ::

            >>> buffer_id = 23
            >>> source = ugentools.SoundIn.ar(bus=(0, 1))
            >>> record_buf = ugentools.RecordBuf.ar(
            ...     buffer_id=buffer_id,
            ...     done_action=0,
            ...     source=source,
            ...     loop=1,
            ...     offset=0,
            ...     pre_level=0,
            ...     rec_level=1,
            ...     run=1,
            ...     trigger=1,
            ...     )
            >>> record_buf.trigger
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]