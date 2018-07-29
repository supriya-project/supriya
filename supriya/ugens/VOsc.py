from supriya.ugens.PureUGen import PureUGen


class VOsc(PureUGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc = supriya.ugens.VOsc.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
        ...     frequency=440,
        ...     phase=0,
        ...     )
        >>> vosc
        VOsc.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'frequency',
        'phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        """
        Constructs an audio-rate VOsc.

        ::

            >>> vosc = supriya.ugens.VOsc.ar(
            ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc
            VOsc.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        """
        Constructs a control-rate VOsc.

        ::

            >>> vosc = supriya.ugens.VOsc.kr(
            ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc
            VOsc.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of VOsc.

        ::

            >>> vosc = supriya.ugens.VOsc.ar(
            ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc.buffer_id
            MouseX.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of VOsc.

        ::

            >>> vosc = supriya.ugens.VOsc.ar(
            ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of VOsc.

        ::

            >>> vosc = supriya.ugens.VOsc.ar(
            ...     buffer_id=supriya.ugens.MouseX.kr(0,7),
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc.phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
