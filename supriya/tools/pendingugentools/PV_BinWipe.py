# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinWipe(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_wipe = ugentools.PV_BinWipe.(
        ...     buffer_a=None,
        ...     buffer_b=None,
        ...     wipe=0,
        ...     )
        >>> pv_bin_wipe

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_a',
        'buffer_b',
        'wipe',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_a=None,
        buffer_b=None,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            wipe=wipe,
            )

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

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_a(self):
        r'''Gets `buffer_a` input of PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe.buffer_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_a')
        return self._inputs[index]

    @property
    def buffer_b(self):
        r'''Gets `buffer_b` input of PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe.buffer_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_b')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_BinWipe.

        ::

            >>> pv_bin_wipe = ugentools.PV_BinWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     wipe=0,
            ...     )
            >>> pv_bin_wipe.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]