# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Dust(UGen):

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

    ### PUBLIC PROPERTIES ###

    @property
    def signal_range(self):
        from supriya.tools import synthdeftools
        return synthdeftools.SignalRange.UNIPOLAR

    ### PUBLIC PROPERTIES ###

    @property
    def density(self):
        r'''Gets `density` input of Dust.

        ::

            >>> density = None
            >>> dust = ugentools.Dust.ar(
            ...     density=density,
            ...     )
            >>> dust.density

        Returns input.
        '''
        index = self._ordered_input_names.index('density')
        return self._inputs[index]