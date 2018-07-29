from supriya.ugens.PureUGen import PureUGen


class LFPulse(PureUGen):
    """
    A non-band-limited pulse oscillator.

    ::

        >>> supriya.ugens.LFPulse.ar()
        LFPulse.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'initial_phase',
        'width',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        initial_phase=0,
        width=0.5,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        initial_phase=0,
        width=0.5,
        ):
        """
        Constructs an audio-rate non-band-limited pulse oscillator.

        ::

            >>> supriya.ugens.LFPulse.ar(
            ...     frequency=[440, 442],
            ...     initial_phase=0.5,
            ...     width=0.1,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        initial_phase=0,
        width=0.5,
        ):
        """
        Constructs an audio-rate non-band-limited pulse oscillator.

        ::

            >>> supriya.ugens.LFPulse.kr(
            ...     frequency=[4, 2],
            ...     initial_phase=0.5,
            ...     width=0.1,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            initial_phase=initial_phase,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of LFPulse.

        ::

            >>> l_f_pulse = supriya.ugens.LFPulse.ar(
            ...     frequency=3,
            ...     initial_phase=0.5,
            ...     width=0.1,
            ...     )
            >>> l_f_pulse.frequency
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        """
        Gets `initial_phase` input of LFPulse.

        ::

            >>> l_f_pulse = supriya.ugens.LFPulse.ar(
            ...     frequency=3,
            ...     initial_phase=0.5,
            ...     width=0.1,
            ...     )
            >>> l_f_pulse.initial_phase
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]

    @property
    def width(self):
        """
        Gets `width` input of LFPulse.

        ::

            >>> l_f_pulse = supriya.ugens.LFPulse.ar(
            ...     frequency=3,
            ...     initial_phase=0.5,
            ...     width=0.1,
            ...     )
            >>> l_f_pulse.width
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]
