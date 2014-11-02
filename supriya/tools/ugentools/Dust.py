# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.SignalRange import SignalRange
from supriya.tools.synthdeftools.UGen import UGen


class Dust(UGen):
    r'''A unipolar random impulse generator.

    ::

        >>> dust = ugentools.Dust.ar(
        ...    density=23,
        ...    )
        >>> dust
        Dust.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'density',
        )

    _signal_range = SignalRange.UNIPOLAR

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
        r'''Creates an audio-rate unipolar random impulse generator.

        ::

            >>> ugentools.Dust.ar(
            ...     density=[1, 2],
            ...     )
            UGenArray({2})

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
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
        r'''Creates a control-rate unipolar random impulse generator.

        ::

            >>> ugentools.Dust.kr(
            ...     density=[1, 2],
            ...     )
            UGenArray({2})

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            density=density,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def density(self):
        r'''Gets `density` input of Dust.

        ::

            >>> density = 0.25
            >>> dust = ugentools.Dust.ar(
            ...     density=density,
            ...     )
            >>> dust.density
            0.25

        Returns input.
        '''
        index = self._ordered_input_names.index('density')
        return self._inputs[index]