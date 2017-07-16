from supriya.tools.ugentools.PureUGen import PureUGen


class SinOscFB(PureUGen):
    """

    ::

        >>> sin_osc_fb = ugentools.SinOscFB.ar(
        ...     feedback=0,
        ...     frequency=440,
        ...     )
        >>> sin_osc_fb
        SinOscFB.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'feedback',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        feedback=0,
        frequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            feedback=feedback,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        feedback=0,
        frequency=440,
        ):
        """
        Constructs an audio-rate SinOscFB.

        ::

            >>> sin_osc_fb = ugentools.SinOscFB.ar(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb
            SinOscFB.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            feedback=feedback,
            frequency=frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        feedback=0,
        frequency=440,
        ):
        """
        Constructs a control-rate SinOscFB.

        ::

            >>> sin_osc_fb = ugentools.SinOscFB.kr(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb
            SinOscFB.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            feedback=feedback,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def feedback(self):
        """
        Gets `feedback` input of SinOscFB.

        ::

            >>> sin_osc_fb = ugentools.SinOscFB.ar(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb.feedback
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('feedback')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of SinOscFB.

        ::

            >>> sin_osc_fb = ugentools.SinOscFB.ar(
            ...     feedback=0,
            ...     frequency=440,
            ...     )
            >>> sin_osc_fb.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]
