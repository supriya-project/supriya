from supriya.ugens.UGen import UGen


class GbmanN(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.

    ::

        >>> gbman_n = supriya.ugens.GbmanN.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ...     )
        >>> gbman_n
        GbmanN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=22050,
        xi=1.2,
        yi=2.1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=22050,
        xi=1.2,
        yi=2.1,
        ):
        """
        Constructs an audio-rate GbmanN.

        ::

            >>> gbman_n = supriya.ugens.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n
            GbmanN.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of GbmanN.

        ::

            >>> gbman_n = supriya.ugens.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of GbmanN.

        ::

            >>> gbman_n = supriya.ugens.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n.xi
            1.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        """
        Gets `yi` input of GbmanN.

        ::

            >>> gbman_n = supriya.ugens.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n.yi
            2.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]
