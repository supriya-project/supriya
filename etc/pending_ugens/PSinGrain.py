from supriya.ugens.UGen import UGen


class PSinGrain(UGen):
    """

    ::

        >>> psin_grain = supriya.ugens.PSinGrain.ar(
        ...     amp=1,
        ...     duration=0.2,
        ...     frequency=440,
        ...     )
        >>> psin_grain
        PSinGrain.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'duration',
        'amp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        amp=1,
        duration=0.2,
        frequency=440,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp=amp,
            duration=duration,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        amp=1,
        duration=0.2,
        frequency=440,
        ):
        """
        Constructs an audio-rate PSinGrain.

        ::

            >>> psin_grain = supriya.ugens.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain
            PSinGrain.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            duration=duration,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def amp(self):
        """
        Gets `amp` input of PSinGrain.

        ::

            >>> psin_grain = supriya.ugens.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain.amp
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('amp')
        return self._inputs[index]

    @property
    def duration(self):
        """
        Gets `duration` input of PSinGrain.

        ::

            >>> psin_grain = supriya.ugens.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain.duration
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of PSinGrain.

        ::

            >>> psin_grain = supriya.ugens.PSinGrain.ar(
            ...     amp=1,
            ...     duration=0.2,
            ...     frequency=440,
            ...     )
            >>> psin_grain.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]
