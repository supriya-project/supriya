# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Dust2(UGen):

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
    def density(self):
        r'''Gets `density` input of Dust2.

        ::

            >>> density = None
            >>> dust_2 = ugentools.Dust2.ar(
            ...     density=density,
            ...     )
            >>> dust_2.density

        Returns input.
        '''
        index = self._ordered_input_names.index('density')
        return self._inputs[index]