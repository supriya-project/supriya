from supriya.ugens.Index import Index


class Shaper(Index):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> shaper = supriya.ugens.Shaper.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        >>> shaper
        Shaper.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        source=None,
        ):
        Index.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        """
        Constructs an audio-rate Shaper.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> shaper = supriya.ugens.Shaper.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> shaper
            Shaper.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        source=None,
        ):
        """
        Constructs a control-rate Shaper.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> shaper = supriya.ugens.Shaper.kr(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> shaper
            Shaper.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of Shaper.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> shaper = supriya.ugens.Shaper.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> shaper.buffer_id

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Shaper.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> shaper = supriya.ugens.Shaper.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> shaper.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
