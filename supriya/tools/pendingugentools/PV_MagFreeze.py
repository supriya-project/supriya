# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagFreeze(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_freeze = ugentools.PV_MagFreeze.(
        ...     )
        >>> pv_mag_freeze

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
        freeze=0,
        ):
        r'''Constructs a PV_MagFreeze.

        ::

            >>> pv_mag_freeze = ugentools.PV_MagFreeze.new(
            ...     buffer_=None,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            freeze=freeze,
            )
        return ugen
