from supriya.ugens.MultiOutUGen import MultiOutUGen


class Hilbert(MultiOutUGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hilbert = supriya.ugens.Hilbert.ar(
        ...     source=source,
        ...     )
        >>> hilbert
        Hilbert.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        """
        Constructs an audio-rate Hilbert.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hilbert = supriya.ugens.Hilbert.ar(
            ...     source=source,
            ...     )
            >>> hilbert
            Hilbert.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of Hilbert.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hilbert = supriya.ugens.Hilbert.ar(
            ...     source=source,
            ...     )
            >>> hilbert.source
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
