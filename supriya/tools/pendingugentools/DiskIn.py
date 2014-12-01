# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class DiskIn(MultiOutUGen):
    r'''

    ::

        >>> disk_in = ugentools.DiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=channel_count,
        ...     loop=0,
        ...     )
        >>> disk_in
        DiskIn.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'buffer_id',
        'loop',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        channel_count=None,
        loop=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            loop=loop,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=buffer_id,
        channel_count=channel_count,
        loop=0,
        ):
        r'''Constructs an audio-rate DiskIn.

        ::

            >>> disk_in = ugentools.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=channel_count,
            ...     loop=0,
            ...     )
            >>> disk_in
            DiskIn.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            loop=loop,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of DiskIn.

        ::

            >>> disk_in = ugentools.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=channel_count,
            ...     loop=0,
            ...     )
            >>> disk_in.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of DiskIn.

        ::

            >>> disk_in = ugentools.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=channel_count,
            ...     loop=0,
            ...     )
            >>> disk_in.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of DiskIn.

        ::

            >>> disk_in = ugentools.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=channel_count,
            ...     loop=0,
            ...     )
            >>> disk_in.loop
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]