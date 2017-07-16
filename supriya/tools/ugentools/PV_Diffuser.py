from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_Diffuser(PV_ChainUGen):
    """
    Shifts phases randomly.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_diffuser = ugentools.PV_Diffuser(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     )
        >>> pv_diffuser
        PV_Diffuser.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        trigger=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        trigger=0,
        ):
        """
        Constructs a PV_Diffuser.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_diffuser = ugentools.PV_Diffuser.new(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     )
            >>> pv_diffuser
            PV_Diffuser.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_Diffuser.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_diffuser = ugentools.PV_Diffuser(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     )
            >>> pv_diffuser.pv_chain
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

    @property
    def trigger(self):
        """
        Gets `trigger` input of PV_Diffuser.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_diffuser = ugentools.PV_Diffuser(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     )
            >>> pv_diffuser.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
