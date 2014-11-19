# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagSmear(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_smear = ugentools.PV_MagSmear.(
        ...     )
        >>> pv_mag_smear

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
        bins=0,
        buffer_=None,
        ):
        r'''Constructs a PV_MagSmear.

        ::

            >>> pv_mag_smear = ugentools.PV_MagSmear.new(
            ...     bins=0,
            ...     buffer_=None,
            ...     )
            >>> pv_mag_smear

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bins=bins,
            buffer_=buffer_,
            )
        return ugen
