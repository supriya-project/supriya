# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb(PV_ChainUGen):
    r'''

    ::

        >>> pv_rect_comb = ugentools.PV_RectComb.(
        ...     buffer_id=None,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ...     )
        >>> pv_rect_comb

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'num_teeth',
        'phase',
        'width',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        r'''Constructs a PV_RectComb.

        ::

            >>> pv_rect_comb = ugentools.PV_RectComb.new(
            ...     buffer_id=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_RectComb.

        ::

            >>> pv_rect_comb = ugentools.PV_RectComb.ar(
            ...     buffer_id=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def num_teeth(self):
        r'''Gets `num_teeth` input of PV_RectComb.

        ::

            >>> pv_rect_comb = ugentools.PV_RectComb.ar(
            ...     buffer_id=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.num_teeth

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('num_teeth')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of PV_RectComb.

        ::

            >>> pv_rect_comb = ugentools.PV_RectComb.ar(
            ...     buffer_id=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of PV_RectComb.

        ::

            >>> pv_rect_comb = ugentools.PV_RectComb.ar(
            ...     buffer_id=None,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.width

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]