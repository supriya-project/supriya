# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagDiv(PV_ChainUGen):
    r'''

    ::

        >>> pv_mag_div = ugentools.PV_MagDiv(
        ...     buffer_a=None,
        ...     buffer_b=None,
        ...     zeroed=0.0001,
        ...     )
        >>> pv_mag_div

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_a',
        'buffer_b',
        'zeroed',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_a=None,
        buffer_b=None,
        zeroed=0.0001,
        ):
        PV_ChainUGen.__init__(
            self,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            zeroed=zeroed,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_a=None,
        buffer_b=None,
        zeroed=0.0001,
        ):
        r'''Constructs a PV_MagDiv.

        ::

            >>> pv_mag_div = ugentools.PV_MagDiv.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     zeroed=0.0001,
            ...     )
            >>> pv_mag_div

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            zeroed=zeroed,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_a(self):
        r'''Gets `buffer_a` input of PV_MagDiv.

        ::

            >>> pv_mag_div = ugentools.PV_MagDiv(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     zeroed=0.0001,
            ...     )
            >>> pv_mag_div.buffer_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_a')
        return self._inputs[index]

    @property
    def buffer_b(self):
        r'''Gets `buffer_b` input of PV_MagDiv.

        ::

            >>> pv_mag_div = ugentools.PV_MagDiv(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     zeroed=0.0001,
            ...     )
            >>> pv_mag_div.buffer_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_b')
        return self._inputs[index]

    @property
    def zeroed(self):
        r'''Gets `zeroed` input of PV_MagDiv.

        ::

            >>> pv_mag_div = ugentools.PV_MagDiv(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     zeroed=0.0001,
            ...     )
            >>> pv_mag_div.zeroed

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('zeroed')
        return self._inputs[index]