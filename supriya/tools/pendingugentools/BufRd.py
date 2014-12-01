# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BufRd(MultiOutUGen):
    r'''

    ::

        >>> buf_rd = ugentools.BufRd.ar(
        ...     buffer_id=0,
        ...     channel_count=channel_count,
        ...     interpolation=2,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> buf_rd
        BufRd.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'buffer_id',
        'phase',
        'loop',
        'interpolation',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        channel_count=None,
        interpolation=2,
        loop=1,
        phase=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            interpolation=interpolation,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        channel_count=None,
        interpolation=2,
        loop=1,
        phase=0,
        ):
        r'''Constructs an audio-rate BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd
            BufRd.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            interpolation=interpolation,
            loop=loop,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=0,
        channel_count=None,
        interpolation=2,
        loop=1,
        phase=0,
        ):
        r'''Constructs a control-rate BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.kr(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd
            BufRd.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            interpolation=interpolation,
            loop=loop,
            phase=phase,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd.buffer_id
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def interpolation(self):
        r'''Gets `interpolation` input of BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd.interpolation
            2.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('interpolation')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd.loop
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of BufRd.

        ::

            >>> buf_rd = ugentools.BufRd.ar(
            ...     buffer_id=0,
            ...     channel_count=channel_count,
            ...     interpolation=2,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> buf_rd.phase
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]