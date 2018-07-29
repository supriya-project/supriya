from supriya.ugens.UGen import UGen


class MostChange(UGen):
    """

    ::

        >>> most_change = supriya.ugens.MostChange.ar(
        ...     a=0,
        ...     b=0,
        ...     )
        >>> most_change
        MostChange.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'a',
        'b',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=0,
        b=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=0,
        b=0,
        ):
        """
        Constructs an audio-rate MostChange.

        ::

            >>> most_change = supriya.ugens.MostChange.ar(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> most_change
            MostChange.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        a=0,
        b=0,
        ):
        """
        Constructs a control-rate MostChange.

        ::

            >>> most_change = supriya.ugens.MostChange.kr(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> most_change
            MostChange.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        """
        Gets `a` input of MostChange.

        ::

            >>> most_change = supriya.ugens.MostChange.ar(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> most_change.a
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        """
        Gets `b` input of MostChange.

        ::

            >>> most_change = supriya.ugens.MostChange.ar(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> most_change.b
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b')
        return self._inputs[index]
