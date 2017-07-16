from supriya.tools.ugentools.PureUGen import PureUGen


class LFCub(PureUGen):
    """
    A sine-like oscillator unit generator.

    ::

        >>> ugentools.LFCub.ar()
        LFCub.ar()

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
        Constructs an audio-rate sine-like oscillator.

        ::

            >>> ugentools.LFCub.ar(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFCub.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        Constructs a control-rate sine-like oscillator.

        ::

            >>> ugentools.LFCub.kr(
            ...     frequency=443,
            ...     initial_phase=0.25,
            ...     )
            LFCub.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        Gets `frequency` input of LFCub.

        ::

            >>> frequency = 442
            >>> lfcub = ugentools.LFCub.ar(
            ...     frequency=frequency,
            ...     )
            >>> lfcub.frequency
            442.0

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def initial_phase(self):
        """
        Gets `initial_phase` input of LFCub.

        ::

            >>> initial_phase = 0.5
            >>> lfcub = ugentools.LFCub.ar(
            ...     initial_phase=initial_phase,
            ...     )
            >>> lfcub.initial_phase
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('initial_phase')
        return self._inputs[index]
