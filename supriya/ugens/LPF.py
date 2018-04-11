from supriya.ugens.Filter import Filter


class LPF(Filter):
    """
    A lowpass filter unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.LPF.ar(source=source)
        LPF.ar()

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
        Constructs an audio-rate lowpass filter.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.LPF.ar(
            ...     frequency=440,
            ...     source=source,
            ...     )
            LPF.ar()

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
        Constructs a control-rate lowpass filter.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> supriya.ugens.LPF.kr(
            ...     frequency=440,
            ...     source=source,
            ...     )
            LPF.kr()

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
        Gets `frequency` input of LPF.

        ::

            >>> frequency = 442
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> lpf = supriya.ugens.LPF.ar(
            ...     frequency=frequency,
            ...     source=source,
            ...     )
            >>> lpf.frequency
            442.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of LPF.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> lpf = supriya.ugens.LPF.ar(
            ...     source=source,
            ...     )
            >>> lpf.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
