# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.synthdeftools.UGen import UGen


class SpecPcile(UGen):
    r'''Find a percentile of FFT magnitude spectrum.

    ::

        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> pv_chain = ugentools.FFT(source=source)
        >>> spec_pcile = ugentools.SpecPcile.kr(
        ...     pv_chain=pv_chain,
        ...     fraction=0.5,
        ...     interpolate=0,
        ...     )
        >>> spec_pcile
        SpecPcile.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'fraction',
        'interpolate',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        fraction=0.5,
        interpolate=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            fraction=fraction,
            interpolate=interpolate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        fraction=0.5,
        interpolate=0,
        ):
        r'''Constructs a control-rate SpecPcile.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> spec_pcile = ugentools.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile
            SpecPcile.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            fraction=fraction,
            interpolate=interpolate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of SpecPcile.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> spec_pcile = ugentools.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.pv_chain
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
                        source=In(
                            bus=OutputProxy(
                                source=NumOutputBuses(
                                    calculation_rate=<CalculationRate.SCALAR: 0>
                                    ),
                                output_index=0
                                ),
                            calculation_rate=<CalculationRate.AUDIO: 2>,
                            channel_count=1
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
    def fraction(self):
        r'''Gets `fraction` input of SpecPcile.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> spec_pcile = ugentools.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.fraction
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('fraction')
        return self._inputs[index]

    @property
    def interpolate(self):
        r'''Gets `interpolate` input of SpecPcile.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> spec_pcile = ugentools.SpecPcile.kr(
            ...     pv_chain=pv_chain,
            ...     fraction=0.5,
            ...     interpolate=0,
            ...     )
            >>> spec_pcile.interpolate
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('interpolate')
        return self._inputs[index]