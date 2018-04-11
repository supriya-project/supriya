from supriya.ugens.UGen import UGen


class LinCongC(UGen):
    """
    A cubic-interpolating linear congruential chaotic generator.

    ::

        >>> lin_cong_c = supriya.ugens.LinCongC.ar(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ...     )
        >>> lin_cong_c
        LinCongC.ar()

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
        Constructs an audio-rate LinCongC.

        ::

            >>> lin_cong_c = supriya.ugens.LinCongC.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_c
            LinCongC.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        Gets `a` input of LinCongC.

        ::

            >>> lin_cong_c = supriya.ugens.LinCongC.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_c.a
            1.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def c(self):
        """
        Gets `c` input of LinCongC.

        ::

            >>> lin_cong_c = supriya.ugens.LinCongC.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_c.c
            0.13

        Returns ugen input.
        """
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of LinCongC.

        ::

            >>> lin_cong_c = supriya.ugens.LinCongC.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_c.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def m(self):
        """
        Gets `m` input of LinCongC.

        ::

            >>> lin_cong_c = supriya.ugens.LinCongC.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_c.m
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('m')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of LinCongC.

        ::

            >>> lin_cong_c = supriya.ugens.LinCongC.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_c.xi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]
