from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Rotate2(MultiOutUGen):
    """
    Equal-power sound-field rotator.

    ::

        >>> x = ugentools.PinkNoise.ar() * 0.4
        >>> y = ugentools.LFTri.ar(frequency=880)
        >>> y *= ugentools.LFPulse.kr(frequency=3, width=0.1)
        >>> position = ugentools.LFSaw.kr(frequency=0.1)
        >>> rotate_2 = ugentools.Rotate2.ar(
        ...     x=x,
        ...     y=y,
        ...     position=position,
        ...     )
        >>> rotate_2
        UGenArray({2})

    Returns an array of the rotator's left and right outputs.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'x',
        'y',
        'position',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        position=0,
        x=None,
        y=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=2,
            position=position,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        position=0,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            position=position,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        position=0,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            position=position,
            x=x,
            y=y,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def position(self):
        """
        Gets `position` property of Rotate2.

        ::

            >>> x = ugentools.PinkNoise.ar() * 0.4
            >>> y = ugentools.LFTri.ar(frequency=880)
            >>> y *= ugentools.LFPulse.kr(frequency=3, width=0.1)
            >>> position = ugentools.LFSaw.kr(frequency=0.1)
            >>> rotate_2 = ugentools.Rotate2.ar(
            ...     x=x,
            ...     y=y,
            ...     position=position,
            ...     )
            >>> rotate_2[0].source.position
            OutputProxy(
                source=LFSaw(
                    calculation_rate=CalculationRate.CONTROL,
                    frequency=0.1,
                    initial_phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def x(self):
        """
        Gets `x` input of Rotate2.

        ::

            >>> x = ugentools.PinkNoise.ar() * 0.4
            >>> y = ugentools.LFTri.ar(frequency=880)
            >>> y *= ugentools.LFPulse.kr(frequency=3, width=0.1)
            >>> position = ugentools.LFSaw.kr(frequency=0.1)
            >>> rotate_2 = ugentools.Rotate2.ar(
            ...     x=x,
            ...     y=y,
            ...     position=position,
            ...     )
            >>> rotate_2[0].source.x
            OutputProxy(
                source=BinaryOpUGen(
                    left=OutputProxy(
                        source=PinkNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        ),
                    right=0.4,
                    calculation_rate=CalculationRate.AUDIO,
                    special_index=2
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('x')
        return self._inputs[index]

    @property
    def y(self):
        """
        Gets `y` input of Rotate2.

        ::

            >>> x = ugentools.PinkNoise.ar() * 0.4
            >>> y = ugentools.LFTri.ar(frequency=880)
            >>> y *= ugentools.LFPulse.kr(frequency=3, width=0.1)
            >>> position = ugentools.LFSaw.kr(frequency=0.1)
            >>> rotate_2 = ugentools.Rotate2.ar(
            ...     x=x,
            ...     y=y,
            ...     position=position,
            ...     )
            >>> rotate_2[0].source.y
            OutputProxy(
                source=BinaryOpUGen(
                    left=OutputProxy(
                        source=LFTri(
                            calculation_rate=CalculationRate.AUDIO,
                            frequency=880.0,
                            initial_phase=0.0
                            ),
                        output_index=0
                        ),
                    right=OutputProxy(
                        source=LFPulse(
                            calculation_rate=CalculationRate.CONTROL,
                            frequency=3.0,
                            initial_phase=0.0,
                            width=0.1
                            ),
                        output_index=0
                        ),
                    calculation_rate=CalculationRate.AUDIO,
                    special_index=2
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('y')
        return self._inputs[index]
