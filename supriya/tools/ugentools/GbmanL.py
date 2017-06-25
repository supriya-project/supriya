from supriya.tools.ugentools.UGen import UGen


class GbmanL(UGen):
    """
    A non-interpolating gingerbreadman map chaotic generator.

    ::

        >>> gbman_l = ugentools.GbmanL.ar(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ...     )
        >>> gbman_l
        GbmanL.ar()

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
        Constructs an audio-rate GbmanL.

        ::

            >>> gbman_l = ugentools.GbmanL.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_l
            GbmanL.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        Gets `frequency` input of GbmanL.

        ::

            >>> gbman_l = ugentools.GbmanL.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_l.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of GbmanL.

        ::

            >>> gbman_l = ugentools.GbmanL.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_l.xi
            1.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        """
        Gets `yi` input of GbmanL.

        ::

            >>> gbman_l = ugentools.GbmanL.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_l.yi
            2.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]
