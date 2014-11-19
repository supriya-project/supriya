# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ChaosGen import ChaosGen


class GbmanN(ChaosGen):
    r'''

    ::

        >>> gbman_n = ugentools.GbmanN.(
        ...     frequency=22050,
        ...     xi=1.2,
        ...     yi=2.1,
        ...     )
        >>> gbman_n

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

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
        ChaosGen.__init__(
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
        r'''Constructs an audio-rate GbmanN.

        ::

            >>> gbman_n = ugentools.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n

        Returns ugen graph.
        '''
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
        r'''Gets `frequency` input of GbmanN.

        ::

            >>> gbman_n = ugentools.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def xi(self):
        r'''Gets `xi` input of GbmanN.

        ::

            >>> gbman_n = ugentools.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n.xi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        r'''Gets `yi` input of GbmanN.

        ::

            >>> gbman_n = ugentools.GbmanN.ar(
            ...     frequency=22050,
            ...     xi=1.2,
            ...     yi=2.1,
            ...     )
            >>> gbman_n.yi

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]