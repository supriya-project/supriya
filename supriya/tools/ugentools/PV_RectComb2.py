from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb2(PV_ChainUGen):
    """
    Makes gaps in the spectrum.

    ::

        >>> pv_chain_a = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = ugentools.FFT(
        ...     source=ugentools.LFSaw.ar(),
        ...     )
        >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     num_teeth=0,
        ...     phase=0,
        ...     width=0.5,
        ...     )
        >>> pv_rect_comb_2
        PV_RectComb2.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain_a',
        'pv_chain_b',
        'num_teeth',
        'phase',
        'width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain_a=None,
        pv_chain_b=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain_a=None,
        pv_chain_b=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        """
        Constructs a PV_RectComb2.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rect_comb_2 = ugentools.PV_RectComb2.new(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2
            PV_RectComb2.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain_a(self):
        """
        Gets `pv_chain_a` input of PV_RectComb2.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.pv_chain_a
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
        index = self._ordered_input_names.index('pv_chain_a')
        return self._inputs[index]

    @property
    def pv_chain_b(self):
        """
        Gets `pv_chain_b` input of PV_RectComb2.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.pv_chain_b
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
                        source=LFSaw(
                            calculation_rate=CalculationRate.AUDIO,
                            frequency=440.0,
                            initial_phase=0.0
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
        index = self._ordered_input_names.index('pv_chain_b')
        return self._inputs[index]

    @property
    def num_teeth(self):
        """
        Gets `num_teeth` input of PV_RectComb2.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.num_teeth
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('num_teeth')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of PV_RectComb2.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]

    @property
    def width(self):
        """
        Gets `width` input of PV_RectComb2.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rect_comb_2 = ugentools.PV_RectComb2(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     num_teeth=0,
            ...     phase=0,
            ...     width=0.5,
            ...     )
            >>> pv_rect_comb_2.width
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]
