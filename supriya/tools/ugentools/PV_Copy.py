# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_Copy(PV_ChainUGen):
    r'''Copies an FFT buffer.

    ::

        >>> fft_a = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> fft_b = ugentools.FFT(
        ...     source=ugentools.LFSaw.ar(),
        ...     )
        >>> pv_copy = ugentools.PV_Copy(
        ...     pv_chain_a=fft_a,
        ...     pv_chain_b=fft_b,
        ...     )
        >>> pv_copy
        PV_Copy.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain_a',
        'pv_chain_b',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain_a=None,
        pv_chain_b=None,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain_a=None,
        pv_chain_b=None,
        ):
        r'''Constructs a PV_Copy.

        ::

            >>> fft_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> fft_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_copy = ugentools.PV_Copy.new(
            ...     pv_chain_a=fft_a,
            ...     pv_chain_b=fft_b,
            ...     )
            >>> pv_copy
            PV_Copy.kr()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain_a(self):
        r'''Gets `pv_chain_a` input of PV_Copy.

        ::

            >>> fft_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> fft_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_copy = ugentools.PV_Copy(
            ...     pv_chain_a=fft_a,
            ...     pv_chain_b=fft_b,
            ...     )
            >>> pv_copy.pv_chain_a
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
                    calculation_rate=<CalculationRate.CONTROL: 1>,
                    active=1.0,
                    hop=0.5,
                    window_size=0.0,
                    window_type=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain_a')
        return self._inputs[index]

    @property
    def pv_chain_b(self):
        r'''Gets `pv_chain_b` input of PV_Copy.

        ::

            >>> fft_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> fft_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_copy = ugentools.PV_Copy(
            ...     pv_chain_a=fft_a,
            ...     pv_chain_b=fft_b,
            ...     )
            >>> pv_copy.pv_chain_b
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
                        source=LFSaw(
                            calculation_rate=<CalculationRate.AUDIO: 2>,
                            frequency=440.0,
                            initial_phase=0.0
                            ),
                        output_index=0
                        ),
                    calculation_rate=<CalculationRate.CONTROL: 1>,
                    active=1.0,
                    hop=0.5,
                    window_size=0.0,
                    window_type=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('pv_chain_b')
        return self._inputs[index]