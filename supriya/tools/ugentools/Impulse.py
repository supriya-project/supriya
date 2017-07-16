from supriya.tools.ugentools.PureUGen import PureUGen


class Impulse(PureUGen):
    """
    A non-band-limited single-sample impulse generator unit generator.

    ::

        >>> ugentools.Impulse.ar()
        Impulse.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'phase',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440.,
        phase=0.,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        phase=0,
        ):
        """
        Constructs an audio-rate non-band-limited single-sample impulse
        generator.

        ::

            >>> ugentools.Impulse.ar(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            Impulse.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        phase=0,
        ):
        """
        Constructs a control-rate non-band-limited single-sample impulse
        generator.

        ::

            >>> ugentools.Impulse.kr(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            Impulse.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of Impulse.

        ::

            >>> frequency = 0.5
            >>> impulse = ugentools.Impulse.ar(
            ...     frequency=frequency,
            ...     )
            >>> impulse.frequency
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of Impulse.

        ::

            >>> phase = 0.25
            >>> impulse = ugentools.Impulse.ar(
            ...     phase=phase,
            ...     )
            >>> impulse.phase
            0.25

        Returns input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
