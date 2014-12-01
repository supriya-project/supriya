# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PlayBuf(MultiOutUGen):
    r'''

    ::

        >>> play_buf = ugentools.PlayBuf.ar(
        ...     buffer_id=0,
        ...     channel_count=channel_count,
        ...     done_action=0,
        ...     loop=0,
        ...     rate=1,
        ...     start_pos=0,
        ...     trigger=1,
        ...     )
        >>> play_buf
        PlayBuf.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'buffer_id',
        'rate',
        'trigger',
        'start_pos',
        'loop',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_pos=0,
        trigger=1,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_pos=start_pos,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_pos=0,
        trigger=1,
        ):
        r'''Constructs an audio-rate PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf
            PlayBuf.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_pos=start_pos,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=0,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_pos=0,
        trigger=1,
        ):
        r'''Constructs a control-rate PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.kr(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf
            PlayBuf.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_pos=start_pos,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.buffer_id
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def done_action(self):
        r'''Gets `done_action` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.done_action
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.loop
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def rate(self):
        r'''Gets `rate` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.rate
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def start_pos(self):
        r'''Gets `start_pos` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.start_pos
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('start_pos')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PlayBuf.

        ::

            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_pos=0,
            ...     trigger=1,
            ...     )
            >>> play_buf.trigger
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]