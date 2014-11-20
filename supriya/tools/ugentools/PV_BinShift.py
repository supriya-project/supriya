# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinShift(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_shift = ugentools.PV_BinShift(
        ...     pv_chain=None,
        ...     interpolate=0,
        ...     shift=0,
        ...     stretch=1,
        ...     )
        >>> pv_bin_shift

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'stretch',
        'shift',
        'interpolate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        interpolate=0,
        shift=0,
        stretch=1,
        ):
        r'''Constructs a PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift.new(
            ...     pv_chain=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            interpolate=interpolate,
            shift=shift,
            stretch=stretch,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.pv_chain

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def interpolate(self):
        r'''Gets `interpolate` input of PV_BinShift.

        ::

            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=None,
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

            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=None,
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

            >>> pv_bin_shift = ugentools.PV_BinShift(
            ...     pv_chain=None,
            ...     interpolate=0,
            ...     shift=0,
            ...     stretch=1,
            ...     )
            >>> pv_bin_shift.stretch

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('stretch')
        return self._inputs[index]