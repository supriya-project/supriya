from supriya.ugens.PureUGen import PureUGen


class LFSaw(PureUGen):
    """
    A non-band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.LFSaw.ar()
        LFSaw.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'initial_phase',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440.,
        initial_phase=0.,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        initial_phase=0,
        ):
        """
        Constructs an audio-rate non-band-limited sawtooth oscillator.

        ::

            >>> supriya.ugens.LFSaw.ar(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFSaw.ar()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        initial_phase=0,
        ):
        """
        Constructs a control-rate non-band-limited sawtooth oscillator.

        ::

            >>> supriya.ugens.LFSaw.kr(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFSaw.kr()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of LFSaw.

        ::

            >>> frequency = 442
            >>> l_f_saw = supriya.ugens.LFSaw.ar(
            ...     frequency=frequency,
            ...     )
            >>> l_f_saw.frequency
            442.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        """
        Gets `initial_phase` input of LFSaw.

        ::

            >>> initial_phase = 0.5
            >>> l_f_saw = supriya.ugens.LFSaw.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> l_f_saw.initial_phase
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]
