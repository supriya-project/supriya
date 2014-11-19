# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagSquared import PV_MagSquared


class PV_MagNoise(PV_MagSquared):
    r'''

    ::

        >>> pv_mag_noise = ugentools.PV_MagNoise.(
        ...     )
        >>> pv_mag_noise

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_=None,
        ):
        r'''Constructs a PV_MagNoise.

        ::

            >>> pv_mag_noise = ugentools.PV_MagNoise.new(
            ...     buffer_=None,
            ...     )
            >>> pv_mag_noise

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            )
        return ugen
