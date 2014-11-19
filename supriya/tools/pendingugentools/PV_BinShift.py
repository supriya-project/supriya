# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_shift = ugentools.PV_BinShift.(
        ...     buffer_id=None,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ...     )
        >>> pv_bin_shift

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'stretch',
        'shift',
        'interpolate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        r'''Constructs a PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.new(
            ...     buffer_id=None,
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
            buffer_id=buffer_id,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.ar(
            ...     buffer_id=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def interpolate(self):
        r'''Gets `interpolate` input of PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.ar(
            ...     buffer_id=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.interpolate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]

    @property
    def shift(self):
        r'''Gets `shift` input of PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.ar(
            ...     buffer_id=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.shift

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('shift')
        return self._inputs[index]

    @property
    def stretch(self):
        r'''Gets `stretch` input of PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.ar(
            ...     buffer_id=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.stretch

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('stretch')
        return self._inputs[index]