from supriya.tools.ugentools.PureUGen import PureUGen


class VOsc3(PureUGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc_3 = ugentools.VOsc3.ar(
        ...     buffer_id=ugentools.MouseX.kr(0,7),
        ...     freq_1=110,
        ...     freq_2=220,
        ...     freq_3=440,
        ...     )
        >>> vosc_3
        VOsc3.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'freq_1',
        'freq_2',
        'freq_3',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        """
        Constructs an audio-rate VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     buffer_id=ugentools.MouseX.kr(0,7),
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3
            VOsc3.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        """
        Constructs a control-rate VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.kr(
            ...     buffer_id=ugentools.MouseX.kr(0,7),
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3
            VOsc3.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     buffer_id=ugentools.MouseX.kr(0,7),
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.buffer_id
            OutputProxy(
                source=MouseX(
                    calculation_rate=CalculationRate.CONTROL,
                    lag=0.0,
                    maximum=7.0,
                    minimum=0.0,
                    warp=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def freq_1(self):
        """
        Gets `freq_1` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     buffer_id=ugentools.MouseX.kr(0,7),
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.freq_1
            110.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freq_1')
        return self._inputs[index]

    @property
    def freq_2(self):
        """
        Gets `freq_2` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     buffer_id=ugentools.MouseX.kr(0,7),
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.freq_2
            220.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freq_2')
        return self._inputs[index]

    @property
    def freq_3(self):
        """
        Gets `freq_3` input of VOsc3.

        ::

            >>> vosc_3 = ugentools.VOsc3.ar(
            ...     buffer_id=ugentools.MouseX.kr(0,7),
            ...     freq_1=110,
            ...     freq_2=220,
            ...     freq_3=440,
            ...     )
            >>> vosc_3.freq_3
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freq_3')
        return self._inputs[index]
