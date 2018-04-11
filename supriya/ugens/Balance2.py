from supriya.ugens.MultiOutUGen import MultiOutUGen


class Balance2(MultiOutUGen):
    """
    A stereo signal balancer.

    ::

        >>> left = supriya.ugens.WhiteNoise.ar()
        >>> right = supriya.ugens.SinOsc.ar()
        >>> balance_2 = supriya.ugens.Balance2.ar(
        ...     left=left,
        ...     level=1,
        ...     position=0,
        ...     right=right,
        ...     )
        >>> balance_2
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'left',
        'right',
        'position',
        'level',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        left=None,
        level=1,
        position=0,
        right=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=2,
            left=left,
            level=level,
            position=position,
            right=right,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        left=None,
        level=1,
        position=0,
        right=None,
        ):
        """
        Constructs an audio-rate Balance2.

        ::

            >>> left = supriya.ugens.WhiteNoise.ar()
            >>> right = supriya.ugens.SinOsc.ar()
            >>> balance_2 = supriya.ugens.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            position=position,
            right=right,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        left=None,
        level=1,
        position=0,
        right=None,
        ):
        """
        Constructs a control-rate Balance2.

        ::

            >>> left = supriya.ugens.WhiteNoise.kr()
            >>> right = supriya.ugens.SinOsc.kr()
            >>> balance_2 = supriya.ugens.Balance2.kr(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            position=position,
            right=right,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def left(self):
        """
        Gets `left` input of Balance2.

        ::

            >>> left = supriya.ugens.WhiteNoise.ar()
            >>> right = supriya.ugens.SinOsc.ar()
            >>> balance_2 = supriya.ugens.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2[0].source.left
            WhiteNoise.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('left')
        return self._inputs[index]

    @property
    def level(self):
        """
        Gets `level` input of Balance2.

        ::

            >>> left = supriya.ugens.WhiteNoise.ar()
            >>> right = supriya.ugens.SinOsc.ar()
            >>> balance_2 = supriya.ugens.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2[0].source.level
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def position(self):
        """
        Gets `position` input of Balance2.

        ::

            >>> left = supriya.ugens.WhiteNoise.ar()
            >>> right = supriya.ugens.SinOsc.ar()
            >>> balance_2 = supriya.ugens.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0.5,
            ...     right=right,
            ...     )
            >>> balance_2[0].source.position
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def right(self):
        """
        Gets `right` input of Balance2.

        ::

            >>> left = supriya.ugens.WhiteNoise.ar()
            >>> right = supriya.ugens.SinOsc.ar()
            >>> balance_2 = supriya.ugens.Balance2.ar(
            ...     left=left,
            ...     level=1,
            ...     position=0,
            ...     right=right,
            ...     )
            >>> balance_2[0].source.right
            SinOsc.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('right')
        return self._inputs[index]
