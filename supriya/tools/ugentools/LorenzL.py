# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class LorenzL(UGen):
    r"""
    A linear-interpolating Lorenz chaotic generator.

    ::

        >>> lorenz_l = ugentools.LorenzL.ar(
        ...     b=2.667,
        ...     frequency=22050,
        ...     h=0.05,
        ...     r=28,
        ...     s=10,
        ...     xi=0.1,
        ...     yi=0,
        ...     zi=0,
        ...     )
        >>> lorenz_l
        LorenzL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        's',
        'r',
        'b',
        'h',
        'xi',
        'yi',
        'zi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        b=2.667,
        frequency=22050,
        h=0.05,
        r=28,
        s=10,
        xi=0.1,
        yi=0,
        zi=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            b=b,
            frequency=frequency,
            h=h,
            r=r,
            s=s,
            xi=xi,
            yi=yi,
            zi=zi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        b=2.667,
        frequency=22050,
        h=0.05,
        r=28,
        s=10,
        xi=0.1,
        yi=0,
        zi=0,
        ):
        r"""
        Constructs an audio-rate LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l
            LorenzL.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            b=b,
            frequency=frequency,
            h=h,
            r=r,
            s=s,
            xi=xi,
            yi=yi,
            zi=zi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def b(self):
        r"""
        Gets `b` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.b
            2.667

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b')
        return self._inputs[index]

    @property
    def frequency(self):
        r"""
        Gets `frequency` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def h(self):
        r"""
        Gets `h` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.h
            0.05

        Returns ugen input.
        """
        index = self._ordered_input_names.index('h')
        return self._inputs[index]

    @property
    def r(self):
        r"""
        Gets `r` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.r
            28.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('r')
        return self._inputs[index]

    @property
    def s(self):
        r"""
        Gets `s` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.s
            10.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('s')
        return self._inputs[index]

    @property
    def xi(self):
        r"""
        Gets `xi` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.xi
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        r"""
        Gets `yi` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.yi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]

    @property
    def zi(self):
        r"""
        Gets `zi` input of LorenzL.

        ::

            >>> lorenz_l = ugentools.LorenzL.ar(
            ...     b=2.667,
            ...     frequency=22050,
            ...     h=0.05,
            ...     r=28,
            ...     s=10,
            ...     xi=0.1,
            ...     yi=0,
            ...     zi=0,
            ...     )
            >>> lorenz_l.zi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('zi')
        return self._inputs[index]
