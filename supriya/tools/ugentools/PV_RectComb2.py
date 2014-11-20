# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb2(PV_ChainUGen):
    r'''

    ::

        >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
        ...     buffer_a=None,
        ...     buffer_b=None,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ...     )
        >>> pv_rect_comb_2

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_a',
        'buffer_b',
        'num_teeth',
        'phase',
        'width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_a=None,
        buffer_b=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        PV_ChainUGen.__init__(
            self,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_a=None,
        buffer_b=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        r'''Constructs a PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_a(self):
        r'''Gets `buffer_a` input of PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.buffer_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_a')
        return self._inputs[index]

    @property
    def buffer_b(self):
        r'''Gets `buffer_b` input of PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.buffer_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_b')
        return self._inputs[index]

    @property
    def num_teeth(self):
        r'''Gets `num_teeth` input of PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.num_teeth

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('num_teeth')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of PV_RectComb2.

        ::

            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.width

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]