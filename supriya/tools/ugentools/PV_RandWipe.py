# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RandWipe(PV_ChainUGen):
    """
    Crossfades in random bin order.

    ::

        >>> pv_chain_a = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_chain_b = ugentools.FFT(
        ...     source=ugentools.LFSaw.ar(),
        ...     )
        >>> pv_rand_wipe = ugentools.PV_RandWipe(
        ...     pv_chain_a=pv_chain_a,
        ...     pv_chain_b=pv_chain_b,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_wipe
        PV_RandWipe.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain_a',
        'pv_chain_b',
        'wipe',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain_a=None,
        pv_chain_b=None,
        trigger=0,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            trigger=trigger,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain_a=None,
        pv_chain_b=None,
        trigger=0,
        wipe=0,
        ):
        """
        Constructs a PV_RandWipe.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rand_wipe = ugentools.PV_RandWipe.new(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe
            PV_RandWipe.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain_a=pv_chain_a,
            pv_chain_b=pv_chain_b,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain_a(self):
        """
        Gets `pv_chain_a` input of PV_RandWipe.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rand_wipe = ugentools.PV_RandWipe(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.pv_chain_a
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
        Gets `pv_chain_b` input of PV_RandWipe.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rand_wipe = ugentools.PV_RandWipe(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.pv_chain_b
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
    def trigger(self):
        """
        Gets `trigger` input of PV_RandWipe.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rand_wipe = ugentools.PV_RandWipe(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def wipe(self):
        """
        Gets `wipe` input of PV_RandWipe.

        ::

            >>> pv_chain_a = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_chain_b = ugentools.FFT(
            ...     source=ugentools.LFSaw.ar(),
            ...     )
            >>> pv_rand_wipe = ugentools.PV_RandWipe(
            ...     pv_chain_a=pv_chain_a,
            ...     pv_chain_b=pv_chain_b,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.wipe
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]
