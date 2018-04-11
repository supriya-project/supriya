from supriya.ugens.UGen import UGen


class LinCongL(UGen):
    """
    A linear-interpolating linear congruential chaotic generator.

    ::

        >>> lin_cong_l = supriya.ugens.LinCongL.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ...     )
        >>> lin_cong_l
        LinCongL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'a',
        'c',
        'm',
        'xi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1.1,
        c=0.13,
        frequency=22050,
        m=1,
        xi=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            frequency=frequency,
            m=m,
            xi=xi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.1,
        c=0.13,
        frequency=22050,
        m=1,
        xi=0,
        ):
        """
        Constructs an audio-rate LinCongL.

        ::

            >>> lin_cong_l = supriya.ugens.LinCongL.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_l
            LinCongL.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            frequency=frequency,
            m=m,
            xi=xi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        """
        Gets `a` input of LinCongL.

        ::

            >>> lin_cong_l = supriya.ugens.LinCongL.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_l.a
            1.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def c(self):
        """
        Gets `c` input of LinCongL.

        ::

            >>> lin_cong_l = supriya.ugens.LinCongL.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_l.c
            0.13

        Returns ugen input.
        """
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of LinCongL.

        ::

            >>> lin_cong_l = supriya.ugens.LinCongL.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_l.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def m(self):
        """
        Gets `m` input of LinCongL.

        ::

            >>> lin_cong_l = supriya.ugens.LinCongL.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_l.m
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('m')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of LinCongL.

        ::

            >>> lin_cong_l = supriya.ugens.LinCongL.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_l.xi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]
