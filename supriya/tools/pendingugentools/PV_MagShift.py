# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_shift = ugentools.PV_MagShift.(
        ...     )
        >>> pv_mag_shift

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
        shift=0,
        stretch=1,
        ):
        r'''Constructs a PV_MagShift.

        ::

            >>> pv_mag_shift = ugentools.PV_MagShift.new(
            ...     buffer_=None,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_mag_shift

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            shift=shift,
            stretch=stretch,
            )
        return ugen
