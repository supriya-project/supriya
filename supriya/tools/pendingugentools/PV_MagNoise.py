# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagSquared import PV_MagSquared


class PV_MagNoise(PV_MagSquared):
    r'''

    ::

        >>> pv_mag_noise = ugentools.PV_MagNoise.(
        ...     buffer_id=None,
        ...     )
        >>> pv_mag_noise

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        ):
        PV_MagSquared.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        ):
        r'''Constructs a PV_MagNoise.

        ::

            >>> pv_mag_noise = ugentools.PV_MagNoise.new(
            ...     buffer_id=None,
            ...     )
            >>> pv_mag_noise

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_MagNoise.

        ::

            >>> pv_mag_noise = ugentools.PV_MagNoise.ar(
            ...     buffer_id=None,
            ...     )
            >>> pv_mag_noise.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]