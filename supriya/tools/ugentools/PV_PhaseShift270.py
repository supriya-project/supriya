from supriya.tools.ugentools.PV_MagSquared import PV_MagSquared


class PV_PhaseShift270(PV_MagSquared):
    """
    Shifts phase by 270 degrees.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_phase_shift_270 = ugentools.PV_PhaseShift270(
        ...     pv_chain=pv_chain,
        ...     )
        >>> pv_phase_shift_270
        PV_PhaseShift270.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        ):
        PV_MagSquared.__init__(
            self,
            pv_chain=pv_chain,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        ):
        """
        Constructs a PV_PhaseShift270.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_phase_shift_270 = ugentools.PV_PhaseShift270.new(
            ...     pv_chain=pv_chain,
            ...     )
            >>> pv_phase_shift_270
            PV_PhaseShift270.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_PhaseShift270.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_phase_shift_270 = ugentools.PV_PhaseShift270(
            ...     pv_chain=pv_chain,
            ...     )
            >>> pv_phase_shift_270.pv_chain
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
                        source=WhiteNoise(
                            calculation_rate=CalculationRate.AUDIO
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
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]
