from supriya.ugens.UGen import UGen


class LatoocarfianN(UGen):
    """
    A non-interpolating Latoocarfian chaotic generator.

    ::

        >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
        ...     a=1,
        ...     b=3,
        ...     c=0.5,
        ...     d=0.5,
        ...     frequency=22050,
        ...     xi=0.5,
        ...     yi=0.5,
        ...     )
        >>> latoocarfian_n
        LatoocarfianN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'a',
        'b',
        'c',
        'd',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1,
        b=3,
        c=0.5,
        d=0.5,
        frequency=22050,
        xi=0.5,
        yi=0.5,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            c=c,
            d=d,
            frequency=frequency,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1,
        b=3,
        c=0.5,
        d=0.5,
        frequency=22050,
        xi=0.5,
        yi=0.5,
        ):
        """
        Constructs an audio-rate LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n
            LatoocarfianN.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            c=c,
            d=d,
            frequency=frequency,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        """
        Gets `a` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.a
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        """
        Gets `b` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.b
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b')
        return self._inputs[index]

    @property
    def c(self):
        """
        Gets `c` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.c
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def d(self):
        """
        Gets `d` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.d
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('d')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.xi
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        """
        Gets `yi` input of LatoocarfianN.

        ::

            >>> latoocarfian_n = supriya.ugens.LatoocarfianN.ar(
            ...     a=1,
            ...     b=3,
            ...     c=0.5,
            ...     d=0.5,
            ...     frequency=22050,
            ...     xi=0.5,
            ...     yi=0.5,
            ...     )
            >>> latoocarfian_n.yi
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]
