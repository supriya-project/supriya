from supriya.ugens.UGen import UGen


class StandardN(UGen):
    """
    A non-interpolating standard map chaotic generator.

    ::

        >>> standard_n = supriya.ugens.StandardN.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ...     )
        >>> standard_n
        StandardN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'k',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        """
        Constructs an audio-rate StandardN.

        ::

            >>> standard_n = supriya.ugens.StandardN.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_n
            StandardN.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of StandardN.

        ::

            >>> standard_n = supriya.ugens.StandardN.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_n.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def k(self):
        """
        Gets `k` input of StandardN.

        ::

            >>> standard_n = supriya.ugens.StandardN.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_n.k
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('k')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of StandardN.

        ::

            >>> standard_n = supriya.ugens.StandardN.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_n.xi
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        """
        Gets `yi` input of StandardN.

        ::

            >>> standard_n = supriya.ugens.StandardN.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_n.yi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]
