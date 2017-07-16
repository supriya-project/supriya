from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class VDiskIn(MultiOutUGen):
    """
    Streams in audio from a file, with variable rate.

    ::

        >>> buffer_id = 23
        >>> vdisk_in = ugentools.VDiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ...     rate=1,
        ...     send_id=0,
        ...     )
        >>> vdisk_in
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
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
        """
        Constructs an audio-rate VDiskIn.

        ::

            >>> buffer_id = 23
            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in
            UGenArray({2})

        Returns ugen graph.
        """
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
    def buffer_id(self):
        """
        Gets `buffer_id` input of VDiskIn.

        ::

            >>> buffer_id = 23
            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in[0].source.buffer_id
            23.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        """
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def loop(self):
        """
        Gets `loop` input of VDiskIn.

        ::

            >>> buffer_id = 23
            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in[0].source.loop
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def rate(self):
        """
        Gets `rate` input of VDiskIn.

        ::

            >>> buffer_id = 23
            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in[0].source.rate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def send_id(self):
        """
        Gets `send_id` input of VDiskIn.

        ::

            >>> buffer_id = 23
            >>> vdisk_in = ugentools.VDiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     rate=1,
            ...     send_id=0,
            ...     )
            >>> vdisk_in[0].source.send_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('send_id')
        return self._inputs[index]
