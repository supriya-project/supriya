# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class QuadC(UGen):
    """
    A cubic-interpolating general quadratic map chaotic generator.

    ::

        >>> quad_c = ugentools.QuadC.ar(
        ...     a=1,
        ...     b=-1,
        ...     c=-0.75,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> quad_c
        QuadC.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'a',
        'b',
        'c',
        'xi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1,
        b=-1,
        c=-0.75,
        frequency=22050,
        xi=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            c=c,
            frequency=frequency,
            xi=xi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1,
        b=-1,
        c=-0.75,
        frequency=22050,
        xi=0,
        ):
        """
        Constructs an audio-rate QuadC.

        ::

            >>> quad_c = ugentools.QuadC.ar(
            ...     a=1,
            ...     b=-1,
            ...     c=-0.75,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> quad_c
            QuadC.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            c=c,
            frequency=frequency,
            xi=xi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        """
        Gets `a` input of QuadC.

        ::

            >>> quad_c = ugentools.QuadC.ar(
            ...     a=1,
            ...     b=-1,
            ...     c=-0.75,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> quad_c.a
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        """
        Gets `b` input of QuadC.

        ::

            >>> quad_c = ugentools.QuadC.ar(
            ...     a=1,
            ...     b=-1,
            ...     c=-0.75,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> quad_c.b
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b')
        return self._inputs[index]

    @property
    def c(self):
        """
        Gets `c` input of QuadC.

        ::

            >>> quad_c = ugentools.QuadC.ar(
            ...     a=1,
            ...     b=-1,
            ...     c=-0.75,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> quad_c.c
            -0.75

        Returns ugen input.
        """
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of QuadC.

        ::

            >>> quad_c = ugentools.QuadC.ar(
            ...     a=1,
            ...     b=-1,
            ...     c=-0.75,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> quad_c.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of QuadC.

        ::

            >>> quad_c = ugentools.QuadC.ar(
            ...     a=1,
            ...     b=-1,
            ...     c=-0.75,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> quad_c.xi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]
