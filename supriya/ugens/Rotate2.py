from supriya.ugens.MultiOutUGen import MultiOutUGen


class Rotate2(MultiOutUGen):
    """
    Equal-power sound-field rotator.

    ::

        >>> x = supriya.ugens.PinkNoise.ar() * 0.4
        >>> y = supriya.ugens.LFTri.ar(frequency=880)
        >>> y *= supriya.ugens.LFPulse.kr(frequency=3, width=0.1)
        >>> position = supriya.ugens.LFSaw.kr(frequency=0.1)
        >>> rotate_2 = supriya.ugens.Rotate2.ar(
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
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
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

            >>> x = supriya.ugens.PinkNoise.ar() * 0.4
            >>> y = supriya.ugens.LFTri.ar(frequency=880)
            >>> y *= supriya.ugens.LFPulse.kr(frequency=3, width=0.1)
            >>> position = supriya.ugens.LFSaw.kr(frequency=0.1)
            >>> rotate_2 = supriya.ugens.Rotate2.ar(
            ...     x=x,
            ...     y=y,
            ...     position=position,
            ...     )
            >>> rotate_2[0].source.position
            LFSaw.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def x(self):
        """
        Gets `x` input of Rotate2.

        ::

            >>> x = supriya.ugens.PinkNoise.ar() * 0.4
            >>> y = supriya.ugens.LFTri.ar(frequency=880)
            >>> y *= supriya.ugens.LFPulse.kr(frequency=3, width=0.1)
            >>> position = supriya.ugens.LFSaw.kr(frequency=0.1)
            >>> rotate_2 = supriya.ugens.Rotate2.ar(
            ...     x=x,
            ...     y=y,
            ...     position=position,
            ...     )
            >>> rotate_2[0].source.x
            BinaryOpUGen.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('x')
        return self._inputs[index]

    @property
    def y(self):
        """
        Gets `y` input of Rotate2.

        ::

            >>> x = supriya.ugens.PinkNoise.ar() * 0.4
            >>> y = supriya.ugens.LFTri.ar(frequency=880)
            >>> y *= supriya.ugens.LFPulse.kr(frequency=3, width=0.1)
            >>> position = supriya.ugens.LFSaw.kr(frequency=0.1)
            >>> rotate_2 = supriya.ugens.Rotate2.ar(
            ...     x=x,
            ...     y=y,
            ...     position=position,
            ...     )
            >>> rotate_2[0].source.y
            BinaryOpUGen.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('y')
        return self._inputs[index]
