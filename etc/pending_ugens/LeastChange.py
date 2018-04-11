from supriya.tools.ugentools.MostChange import MostChange


class LeastChange(MostChange):
    """

    ::

        >>> least_change = ugentools.LeastChange.ar(
        ...     a=0,
        ...     b=0,
        ...     )
        >>> least_change
        LeastChange.ar()

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
        MostChange.__init__(
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
        Constructs an audio-rate LeastChange.

        ::

            >>> least_change = ugentools.LeastChange.ar(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> least_change
            LeastChange.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        Constructs a control-rate LeastChange.

        ::

            >>> least_change = ugentools.LeastChange.kr(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> least_change
            LeastChange.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
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
        Gets `a` input of LeastChange.

        ::

            >>> least_change = ugentools.LeastChange.ar(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> least_change.a
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        """
        Gets `b` input of LeastChange.

        ::

            >>> least_change = ugentools.LeastChange.ar(
            ...     a=0,
            ...     b=0,
            ...     )
            >>> least_change.b
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b')
        return self._inputs[index]
