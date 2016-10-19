# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class CuspL(UGen):
    r"""
    A linear-interpolating cusp map chaotic generator.

    ::

        >>> cusp_l = ugentools.CuspL.ar(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> cusp_l
        CuspL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'a',
        'b',
        'xi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a=1,
        b=1.9,
        frequency=22050,
        xi=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            frequency=frequency,
            xi=xi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1,
        b=1.9,
        frequency=22050,
        xi=0,
        ):
        r"""
        Constructs an audio-rate CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l
            CuspL.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            frequency=frequency,
            xi=xi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def a(self):
        r"""
        Gets `a` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.a
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        r"""
        Gets `b` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.b
            1.9

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b')
        return self._inputs[index]

    @property
    def frequency(self):
        r"""
        Gets `frequency` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        r"""
        Gets `xi` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.xi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]
