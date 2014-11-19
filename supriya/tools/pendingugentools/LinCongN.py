# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ChaosGen import ChaosGen


class LinCongN(ChaosGen):
    r'''

    ::

        >>> lin_cong_n = ugentools.LinCongN.(
        ...     a=1.1,
        ...     c=0.13,
        ...     frequency=22050,
        ...     m=1,
        ...     xi=0,
        ...     )
        >>> lin_cong_n

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

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
        ChaosGen.__init__(
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
        r'''Constructs an audio-rate LinCongN.

        ::

            >>> lin_cong_n = ugentools.LinCongN.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_n

        Returns ugen graph.
        '''
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
        r'''Gets `a` input of LinCongN.

        ::

            >>> lin_cong_n = ugentools.LinCongN.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_n.a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def c(self):
        r'''Gets `c` input of LinCongN.

        ::

            >>> lin_cong_n = ugentools.LinCongN.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_n.c

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('c')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of LinCongN.

        ::

            >>> lin_cong_n = ugentools.LinCongN.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_n.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def m(self):
        r'''Gets `m` input of LinCongN.

        ::

            >>> lin_cong_n = ugentools.LinCongN.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_n.m

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('m')
        return self._inputs[index]

    @property
    def xi(self):
        r'''Gets `xi` input of LinCongN.

        ::

            >>> lin_cong_n = ugentools.LinCongN.ar(
            ...     a=1.1,
            ...     c=0.13,
            ...     frequency=22050,
            ...     m=1,
            ...     xi=0,
            ...     )
            >>> lin_cong_n.xi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]