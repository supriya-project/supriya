# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb(PV_ChainUGen):
    r'''

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_rect_comb = ugentools.PV_RectComb(
        ...     pv_chain=pv_chain,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ...     )
        >>> pv_rect_comb
        PV_RectComb.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'num_teeth',
        'phase',
        'width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        r'''Constructs a PV_RectComb.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_rect_comb = ugentools.PV_RectComb.new(
            ...     pv_chain=pv_chain,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb
            PV_RectComb.kr()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_RectComb.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_rect_comb = ugentools.PV_RectComb(
            ...     pv_chain=pv_chain,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.pv_chain
            OutputProxy(
                source=FFT(
                    buffer_id=OutputProxy(
                        source=LocalBuf(
                            frame_count=2048.0,
                            channel_count=1.0,
                            calculation_rate=<CalculationRate.SCALAR: 0>
                            ),
                        output_index=0
                        ),
                    source=OutputProxy(
                        source=WhiteNoise(
                            calculation_rate=<CalculationRate.AUDIO: 2>
                            ),
                        output_index=0
                        ),
                    active=1.0,
                    hop=0.5,
                    window_size=0.0,
                    window_type=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def num_teeth(self):
        r'''Gets `num_teeth` input of PV_RectComb.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_rect_comb = ugentools.PV_RectComb(
            ...     pv_chain=pv_chain,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.num_teeth
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('num_teeth')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of PV_RectComb.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_rect_comb = ugentools.PV_RectComb(
            ...     pv_chain=pv_chain,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.phase
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of PV_RectComb.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_rect_comb = ugentools.PV_RectComb(
            ...     pv_chain=pv_chain,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb.width
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]