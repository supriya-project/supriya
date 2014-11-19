# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.StandardN import StandardN


class StandardL(StandardN):
    r'''

    ::

        >>> standard_l = ugentools.StandardL.(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ...     )
        >>> standard_l

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'k',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        StandardN.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        r'''Constructs an audio-rate StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def k(self):
        r'''Gets `k` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.k

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('k')
        return self._inputs[index]

    @property
    def xi(self):
        r'''Gets `xi` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.xi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        r'''Gets `yi` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.yi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]