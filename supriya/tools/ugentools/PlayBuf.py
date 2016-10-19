# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PlayBuf(MultiOutUGen):
    r"""
    A sample playback oscillator.

    ::

        >>> buffer_id = 23
        >>> play_buf = ugentools.PlayBuf.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     done_action=0,
        ...     loop=0,
        ...     rate=1,
        ...     start_position=0,
        ...     trigger=1,
        ...     )
        >>> play_buf
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'rate',
        'trigger',
        'start_position',
        'loop',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_position=0,
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
            start_position=start_position,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_position=0,
        trigger=1,
        ):
        r"""
        Constructs an audio-rate PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_position=start_position,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_position=0,
        trigger=1,
        ):
        r"""
        Constructs a control-rate PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.kr(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_position=start_position,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r"""
        Gets `buffer_id` input of PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf[0].source.buffer_id
            23.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def done_action(self):
        r"""
        Gets `done_action` input of PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf[0].source.done_action
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def loop(self):
        r"""
        Gets `loop` input of PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf[0].source.loop
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        r"""
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def rate(self):
        r"""
        Gets `rate` input of PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf[0].source.rate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def start_position(self):
        r"""
        Gets `start_position` input of PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf[0].source.start_position
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('start_position')
        return self._inputs[index]

    @property
    def trigger(self):
        r"""
        Gets `trigger` input of PlayBuf.

        ::

            >>> buffer_id = 23
            >>> play_buf = ugentools.PlayBuf.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     done_action=0,
            ...     loop=0,
            ...     rate=1,
            ...     start_position=0,
            ...     trigger=1,
            ...     )
            >>> play_buf[0].source.trigger
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
