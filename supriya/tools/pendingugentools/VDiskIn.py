# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class VDiskIn(MultiOutUGen):
    r'''

    ::

        >>> vdisk_in = ugentools.VDiskIn.(
        ...     buffer_id=None,
        ...     channel_count=None,
        ...     loop=0,
        ...     rate=1,
        ...     send_id=0,
        ...     )
        >>> vdisk_in

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'buffer_id',
        'rate',
        'loop',
        'send_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        channel_count=None,
        loop=0,
        rate=1,
        send_id=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            loop=loop,
            rate=rate,
            send_id=send_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        channel_count=None,
        loop=0,
        rate=1,
        send_id=0,
        ):
        r'''Constructs an audio-rate VDiskIn.

        ::

            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=None,
            ...     channel_count=None,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            loop=loop,
            rate=rate,
            send_id=send_id,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of VDiskIn.

        ::

            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=None,
            ...     channel_count=None,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of VDiskIn.

        ::

            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=None,
            ...     channel_count=None,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def rate(self):
        r'''Gets `rate` input of VDiskIn.

        ::

            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=None,
            ...     channel_count=None,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in.rate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def loop(self):
        r'''Gets `loop` input of VDiskIn.

        ::

            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=None,
            ...     channel_count=None,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in.loop

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def send_id(self):
        r'''Gets `send_id` input of VDiskIn.

        ::

            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=None,
            ...     channel_count=None,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in.send_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('send_id')
        return self._inputs[index]