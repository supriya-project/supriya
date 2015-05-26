# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ODFType import ODFType
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.synthdeftools.UGen import UGen


class Onsets(UGen):
    r'''An onset detector.

    ::

        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> pv_chain = ugentools.FFT(source=source)
        >>> onsets = ugentools.Onsets.kr(
        ...     pv_chain=pv_chain,
        ...     floor=0.1,
        ...     medianspan=11,
        ...     mingap=10,
        ...     odftype=ugentools.ODFType.RCOMPLEX,
        ...     rawodf=0,
        ...     relaxtime=1,
        ...     threshold=0.5,
        ...     whtype=1,
        ...     )
        >>> onsets
        Onsets.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'threshold',
        'odftype',
        'relaxtime',
        'floor',
        'mingap',
        'medianspan',
        'whtype',
        'rawodf',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype=ODFType.RCOMPLEX,
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            pv_chain=pv_chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype=ODFType.RCOMPLEX,
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        r'''Constructs a control-rate Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets
            Onsets.kr()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.pv_chain
            OutputProxy(
                source=FFT(
                    buffer_id=OutputProxy(
                        source=LocalBuf(
                            frame_count=2048.0,
                            channel_count=1.0,
                            calculation_rate=CalculationRate.SCALAR
                            ),
                        output_index=0
                        ),
                    source=OutputProxy(
                        source=In(
                            bus=OutputProxy(
                                source=NumOutputBuses(
                                    calculation_rate=CalculationRate.SCALAR
                                    ),
                                output_index=0
                                ),
                            calculation_rate=CalculationRate.AUDIO,
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
    def floor(self):
        r'''Gets `floor` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.floor
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('floor')
        return self._inputs[index]

    @property
    def medianspan(self):
        r'''Gets `medianspan` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.medianspan
            11.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('medianspan')
        return self._inputs[index]

    @property
    def mingap(self):
        r'''Gets `mingap` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.mingap
            10.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('mingap')
        return self._inputs[index]

    @property
    def odftype(self):
        r'''Gets `odftype` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.odftype
            3.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('odftype')
        return self._inputs[index]

    @property
    def rawodf(self):
        r'''Gets `rawodf` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.rawodf
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rawodf')
        return self._inputs[index]

    @property
    def relaxtime(self):
        r'''Gets `relaxtime` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.relaxtime
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('relaxtime')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.threshold
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def whtype(self):
        r'''Gets `whtype` input of Onsets.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> onsets = ugentools.Onsets.kr(
            ...     pv_chain=pv_chain,
            ...     floor=0.1,
            ...     medianspan=11,
            ...     mingap=10,
            ...     odftype=ugentools.ODFType.RCOMPLEX,
            ...     rawodf=0,
            ...     relaxtime=1,
            ...     threshold=0.5,
            ...     whtype=1,
            ...     )
            >>> onsets.whtype
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('whtype')
        return self._inputs[index]