# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagMul(PV_ChainUGen):
    r'''Multiplies FFT magnitudes.

    ::

        >>> fft_a = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> fft_b = ugentools.FFT(
        ...     source=ugentools.LFSaw.ar(),
        ...     )
        >>> pv_mag_mul = ugentools.PV_MagMul(
        ...     buffer_id_a=fft_a,
        ...     buffer_id_b=fft_b,
        ...     )
        >>> pv_mag_mul
        PV_MagMul.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id_a',
        'buffer_id_b',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id_a=None,
        buffer_id_b=None,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id_a=buffer_id_a,
            buffer_id_b=buffer_id_b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id_a=None,
        buffer_id_b=None,
        ):
        r'''Constructs a PV_MagMul.

        ::

            >>> fft_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> fft_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_mag_mul = ugentools.PV_MagMul.new(
            ...     buffer_id_a=fft_a,
            ...     buffer_id_b=fft_b,
            ...     )
            >>> pv_mag_mul
            PV_MagMul.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id_a=buffer_id_a,
            buffer_id_b=buffer_id_b,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id_a(self):
        r'''Gets `buffer_id_a` input of PV_MagMul.

        ::

            >>> fft_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> fft_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_mag_mul = ugentools.PV_MagMul(
            ...     buffer_id_a=fft_a,
            ...     buffer_id_b=fft_b,
            ...     )
            >>> pv_mag_mul.buffer_id_a
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
        index = self._ordered_input_names.index('buffer_id_a')
        return self._inputs[index]

    @property
    def buffer_id_b(self):
        r'''Gets `buffer_id_b` input of PV_MagMul.

        ::

            >>> fft_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> fft_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_mag_mul = ugentools.PV_MagMul(
            ...     buffer_id_a=fft_a,
            ...     buffer_id_b=fft_b,
            ...     )
            >>> pv_mag_mul.buffer_id_b
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
        index = self._ordered_input_names.index('buffer_id_b')
        return self._inputs[index]