from supriya.ugens.PureUGen import PureUGen


class COsc(PureUGen):
    """
    A chorusing wavetable oscillator.

    ::

        >>> cosc = supriya.ugens.COsc.ar(
        ...     beats=0.5,
        ...     buffer_id=23,
        ...     frequency=440,
        ...     )
        >>> cosc
        COsc.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'frequency',
        'beats',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        beats=0.5,
        buffer_id=None,
        frequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            beats=beats,
            buffer_id=buffer_id,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        beats=0.5,
        buffer_id=None,
        frequency=440,
        ):
        """
        Constructs an audio-rate COsc.

        ::

            >>> cosc = supriya.ugens.COsc.ar(
            ...     beats=0.5,
            ...     buffer_id=23,
            ...     frequency=440,
            ...     )
            >>> cosc
            COsc.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            beats=beats,
            buffer_id=buffer_id,
            frequency=frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        beats=0.5,
        buffer_id=None,
        frequency=440,
        ):
        """
        Constructs a control-rate COsc.

        ::

            >>> cosc = supriya.ugens.COsc.kr(
            ...     beats=0.5,
            ...     buffer_id=23,
            ...     frequency=440,
            ...     )
            >>> cosc
            COsc.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            beats=beats,
            buffer_id=buffer_id,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        """
        Gets `beats` input of COsc.

        ::

            >>> cosc = supriya.ugens.COsc.ar(
            ...     beats=0.5,
            ...     buffer_id=23,
            ...     frequency=440,
            ...     )
            >>> cosc.beats
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('beats')
        return self._inputs[index]

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of COsc.

        ::

            >>> cosc = supriya.ugens.COsc.ar(
            ...     beats=0.5,
            ...     buffer_id=23,
            ...     frequency=440,
            ...     )
            >>> cosc.buffer_id
            23

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return int(self._inputs[index])

    @property
    def frequency(self):
        """
        Gets `frequency` input of COsc.

        ::

            >>> cosc = supriya.ugens.COsc.ar(
            ...     beats=0.5,
            ...     buffer_id=23,
            ...     frequency=440,
            ...     )
            >>> cosc.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]
