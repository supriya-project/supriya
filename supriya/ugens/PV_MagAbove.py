from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagAbove(PV_ChainUGen):
    """
    Passes magnitudes above threshold.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_above = supriya.ugens.PV_MagAbove(
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

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_above = supriya.ugens.PV_MagAbove.new(
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

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_above = supriya.ugens.PV_MagAbove(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of PV_MagAbove.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_above = supriya.ugens.PV_MagAbove(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_above.threshold
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]
