# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):
    r'''Shifts phase.

    ::
        
        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> shift = ugentools.LFNoise2.kr(1).scale(-1, 1, -180, 180)
        >>> pv_phase_shift = ugentools.PV_PhaseShift(
        ...     pv_chain=pv_chain,
        ...     integrate=0,
        ...     shift=shift,
        ...     )
        >>> pv_phase_shift
        PV_PhaseShift.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'shift',
        'integrate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        integrate=0,
        shift=None,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            integrate=integrate,
            shift=shift,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        integrate=0,
        shift=None,
        ):
        r'''Constructs a PV_PhaseShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> shift = ugentools.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = ugentools.PV_PhaseShift.new(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift
            PV_PhaseShift.kr()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            integrate=integrate,
            shift=shift,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        r'''Gets `pv_chain` input of PV_PhaseShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> shift = ugentools.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = ugentools.PV_PhaseShift(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift.pv_chain
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
    def integrate(self):
        r'''Gets `integrate` input of PV_PhaseShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> shift = ugentools.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = ugentools.PV_PhaseShift(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift.integrate
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('integrate')
        return self._inputs[index]

    @property
    def shift(self):
        r'''Gets `shift` input of PV_PhaseShift.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> shift = ugentools.LFNoise2.kr(1).scale(-1, 1, -180, 180)
            >>> pv_phase_shift = ugentools.PV_PhaseShift(
            ...     pv_chain=pv_chain,
            ...     integrate=0,
            ...     shift=shift,
            ...     )
            >>> pv_phase_shift.shift
            OutputProxy(
                source=BinaryOpUGen(
                    left=OutputProxy(
                        source=LFNoise2(
                            calculation_rate=<CalculationRate.CONTROL: 1>,
                            frequency=1.0
                            ),
                        output_index=0
                        ),
                    right=180.0,
                    calculation_rate=<CalculationRate.CONTROL: 1>,
                    special_index=2
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('shift')
        return self._inputs[index]