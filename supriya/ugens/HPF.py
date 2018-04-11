from supriya.ugens.Filter import Filter


class HPF(Filter):
    """
    A Highpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.HPF.ar(source=source)
        HPF.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        calculation_rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        source=None,
        ):
        """
        Constructs an audio-rate highpass filter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.HPF.ar(
            ...     frequency=440,
            ...     source=source,
            ...     )
            HPF.ar()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        source=None,
        ):
        """
        Constructs a control-rate highpass filter.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> supriya.ugens.HPF.kr(
            ...     frequency=440,
            ...     source=source,
            ...     )
            HPF.kr()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of HPF.

        ::

            >>> frequency = 442
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hpf = supriya.ugens.HPF.ar(
            ...     frequency=frequency,
            ...     source=source,
            ...     )
            >>> hpf.frequency
            442.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of HPF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hpf = supriya.ugens.HPF.ar(
            ...     source=source,
            ...     )
            >>> hpf.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
