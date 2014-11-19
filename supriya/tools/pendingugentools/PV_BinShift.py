# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_shift = ugentools.PV_BinShift.(
        ...     )
        >>> pv_bin_shift

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
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        r'''Constructs a PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.new(
            ...     buffer_=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )
        return ugen
