from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_HainsworthFoote(PV_ChainUGen):
    """
    A FFT onset detector.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
        ...     pv_chain=pv_chain,
        ...     propf=0,
        ...     proph=0,
        ...     threshold=1,
        ...     waittime=0.04,
        ...     )
        >>> pv_hainsworth_foote
        PV_HainsworthFoote.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'proph',
        'propf',
        'threshold',
        'waittime',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        """
        Constructs an audio-rate PV_HainsworthFoote.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=pv_chain,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote
            PV_HainsworthFoote.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_HainsworthFoote.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=pv_chain,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.pv_chain
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
    def propf(self):
        """
        Gets `propf` input of PV_HainsworthFoote.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=pv_chain,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.propf
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('propf')
        return self._inputs[index]

    @property
    def proph(self):
        """
        Gets `proph` input of PV_HainsworthFoote.

        ::
            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )

            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=pv_chain,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.proph
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('proph')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of PV_HainsworthFoote.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=pv_chain,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.threshold
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]

    @property
    def waittime(self):
        """
        Gets `waittime` input of PV_HainsworthFoote.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_hainsworth_foote = ugentools.PV_HainsworthFoote(
            ...     pv_chain=pv_chain,
            ...     propf=0,
            ...     proph=0,
            ...     threshold=1,
            ...     waittime=0.04,
            ...     )
            >>> pv_hainsworth_foote.waittime
            0.04

        Returns ugen input.
        """
        index = self._ordered_input_names.index('waittime')
        return self._inputs[index]
