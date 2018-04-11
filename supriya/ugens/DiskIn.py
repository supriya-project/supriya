from supriya.ugens.MultiOutUGen import MultiOutUGen


class DiskIn(MultiOutUGen):
    """
    Streams in audio from a file.

    ::

        >>> buffer_id = 23
        >>> disk_in = supriya.ugens.DiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ...     )
        >>> disk_in
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
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
        buffer_id=None,
        channel_count=None,
        loop=0,
        ):
        """
        Constructs an audio-rate DiskIn.

        ::

            >>> buffer_id = 23
            >>> disk_in = supriya.ugens.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     )
            >>> disk_in
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        """
        Gets `buffer_id` input of DiskIn.

        ::

            >>> buffer_id = 23
            >>> disk_in = supriya.ugens.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     )
            >>> disk_in[0].source.buffer_id
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
        Gets `loop` input of DiskIn.

        ::

            >>> buffer_id = 23
            >>> disk_in = supriya.ugens.DiskIn.ar(
            ...     buffer_id=buffer_id,
            ...     channel_count=2,
            ...     loop=0,
            ...     )
            >>> disk_in[0].source.loop
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]
