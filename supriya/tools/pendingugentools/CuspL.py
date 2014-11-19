# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.CuspN import CuspN


class CuspL(CuspN):
    r'''

    ::

        >>> cusp_l = ugentools.CuspL.(
        ...     a=1,
        ...     b=1.9,
        ...     frequency=22050,
        ...     xi=0,
        ...     )
        >>> cusp_l

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

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
        CuspN.__init__(
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
        r'''Constructs an audio-rate CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l

        Returns ugen graph.
        '''
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
        r'''Gets `a` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('a')
        return self._inputs[index]

    @property
    def b(self):
        r'''Gets `b` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('b')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        r'''Gets `xi` input of CuspL.

        ::

            >>> cusp_l = ugentools.CuspL.ar(
            ...     a=1,
            ...     b=1.9,
            ...     frequency=22050,
            ...     xi=0,
            ...     )
            >>> cusp_l.xi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]