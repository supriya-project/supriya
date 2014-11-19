# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinWipe(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_wipe = ugentools.PV_BinWipe.(
        ...     )
        >>> pv_bin_wipe

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
        buffer_a=None,
        buffer_b=None,
        wipe=0,
        ):
        r'''Constructs a PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            wipe=wipe,
            )
        return ugen
