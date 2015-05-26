# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BeatTrack(MultiOutUGen):
    r'''Autocorrelation beat tracker.

    ::

        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> pv_chain = ugentools.FFT(source=source)
        >>> beat_track = ugentools.BeatTrack.kr(
        ...     pv_chain=pv_chain,
        ...     lock=0,
        ...     )
        >>> beat_track
        UGenArray({4})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'lock',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        lock=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=CalculationRate.CONTROL,
            channel_count=4,
            lock=lock,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        lock=0,
        ):
        r'''Constructs a control-rate BeatTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> beat_track = ugentools.BeatTrack.kr(
            ...     pv_chain=pv_chain,
            ...     lock=0,
            ...     )
            >>> beat_track
            UGenArray({4})

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            lock=lock,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of BeatTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> beat_track = ugentools.BeatTrack.kr(
            ...     pv_chain=pv_chain,
            ...     lock=0,
            ...     )
            >>> beat_track[0].source.pv_chain
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
    def lock(self):
        r'''Gets `lock` input of BeatTrack.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> beat_track = ugentools.BeatTrack.kr(
            ...     pv_chain=pv_chain,
            ...     lock=0,
            ...     )
            >>> beat_track[0].source.lock
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lock')
        return self._inputs[index]