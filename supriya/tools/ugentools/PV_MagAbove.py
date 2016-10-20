# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_MagAbove(PV_ChainUGen):
    """
    Passes magnitudes above threshold.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_above = ugentools.PV_MagAbove(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_mag_above
        PV_MagAbove.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'threshold',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        threshold=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            threshold=threshold,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        threshold=0,
        ):
        """
        Constructs a PV_MagAbove.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_above = ugentools.PV_MagAbove.new(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above
            PV_MagAbove.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            threshold=threshold,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_MagAbove.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_above = ugentools.PV_MagAbove(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above.pv_chain
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
    def threshold(self):
        """
        Gets `threshold` input of PV_MagAbove.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_above = ugentools.PV_MagAbove(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above.threshold
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]
