# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Loudness(UGen):
    r'''Extraction of instantaneous loudness in `sones`.

    ::

        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> pv_chain = ugentools.FFT(source=source)
        >>> loudness = ugentools.Loudness.kr(
        ...     pv_chain=pv_chain,
        ...     smask=0.25,
        ...     tmask=1,
        ...     )
        >>> loudness
        Loudness.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Machine Listening UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'smask',
        'tmask',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        pv_chain=None,
        smask=0.25,
        tmask=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            smask=smask,
            tmask=tmask,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        smask=0.25,
        tmask=1,
        ):
        r'''Constructs a control-rate Loudness.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> loudness = ugentools.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness
            Loudness.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            smask=smask,
            tmask=tmask,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of Loudness.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> loudness = ugentools.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.pv_chain
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
    def smask(self):
        r'''Gets `smask` input of Loudness.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> loudness = ugentools.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.smask
            0.25

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('smask')
        return self._inputs[index]

    @property
    def tmask(self):
        r'''Gets `tmask` input of Loudness.

        ::

            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> pv_chain = ugentools.FFT(source=source)
            >>> loudness = ugentools.Loudness.kr(
            ...     pv_chain=pv_chain,
            ...     smask=0.25,
            ...     tmask=1,
            ...     )
            >>> loudness.tmask
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('tmask')
        return self._inputs[index]