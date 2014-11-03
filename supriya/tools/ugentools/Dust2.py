# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Dust2(UGen):
    r'''A bipolar random impulse generator.

    ::

        >>> dust_2 = ugentools.Dust2.ar(
        ...    density=23,
        ...    )
        >>> dust_2
        Dust2.ar()

    '''


    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'density',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        density=0.,
        ):
        UGen.__init__(
            self,
            rate=rate,
            density=density,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        density=0,
        ):
        r'''Creates an audio-rate bipolar random impulse generator.

        ::

            >>> ugentools.Dust2.ar(
            ...     density=[1, 2],
            ...     )
            UGenArray({2})

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            density=density,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        density=0,
        ):
        r'''Creates a control-rate bipolar random impulse generator.

        ::

            >>> ugentools.Dust2.kr(
            ...     density=[1, 2],
            ...     )
            UGenArray({2})

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            density=density,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def density(self):
        r'''Gets `density` input of Dust2.

        ::

            >>> density = 0.25
            >>> dust_2 = ugentools.Dust2.ar(
            ...     density=density,
            ...     )
            >>> dust_2.density
            0.25

        Returns input.
        '''
        index = self._ordered_input_names.index('density')
        return self._inputs[index]