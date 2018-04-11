from supriya.ugens.Filter import Filter


class Resonz(Filter):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> resonz = supriya.ugens.Resonz.ar(
        ...     bwr=1,
        ...     frequency=440,
        ...     source=source,
        ...     )
        >>> resonz
        Resonz.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'bwr',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bwr=1,
        frequency=440,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            bwr=bwr,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bwr=1,
        frequency=440,
        source=None,
        ):
        """
        Constructs an audio-rate Resonz.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> resonz = supriya.ugens.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz
            Resonz.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bwr=bwr,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        bwr=1,
        frequency=440,
        source=None,
        ):
        """
        Constructs a control-rate Resonz.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> resonz = supriya.ugens.Resonz.kr(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz
            Resonz.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bwr=bwr,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bwr(self):
        """
        Gets `bwr` input of Resonz.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> resonz = supriya.ugens.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz.bwr
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bwr')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of Resonz.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> resonz = supriya.ugens.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Resonz.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> resonz = supriya.ugens.Resonz.ar(
            ...     bwr=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> resonz.source
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
