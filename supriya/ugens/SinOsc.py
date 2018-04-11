from supriya.ugens.PureUGen import PureUGen


class SinOsc(PureUGen):
    """
    A sinusoid oscillator unit generator.

    ::

        >>> supriya.ugens.SinOsc.ar()
        SinOsc.ar()

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
        Constructs an audio-rate sinusoid oscillator.

        ::

            >>> supriya.ugens.SinOsc.ar(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            SinOsc.ar()

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
        Constructs a control-rate sinusoid oscillator.

        ::

            >>> supriya.ugens.SinOsc.kr(
            ...     frequency=443,
            ...     phase=0.25,
            ...     )
            SinOsc.kr()

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
        Gets `frequency` input of SinOsc.

        ::

            >>> frequency = 442
            >>> sin_osc = supriya.ugens.SinOsc.ar(
            ...     frequency=frequency,
            ...     )
            >>> sin_osc.frequency
            442.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of SinOsc.

        ::

            >>> phase = 0.5
            >>> sin_osc = supriya.ugens.SinOsc.ar(
            ...     phase=phase,
            ...     )
            >>> sin_osc.phase
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
