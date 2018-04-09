from supriya.tools.ugentools.PV_MagAbove import PV_MagAbove


class PV_MagClip(PV_MagAbove):
    """
    Clips magnitudes.

    ::

        >>> pv_chain = ugentools.FFT(
        ...     source=ugentools.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_clip = ugentools.PV_MagClip(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_mag_clip
        PV_MagClip.kr()

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
        PV_MagAbove.__init__(
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
        Constructs a PV_MagClip.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_clip = ugentools.PV_MagClip.new(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_clip
            PV_MagClip.kr()

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
        Gets `pv_chain` input of PV_MagClip.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_clip = ugentools.PV_MagClip(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_clip.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of PV_MagClip.

        ::

            >>> pv_chain = ugentools.FFT(
            ...     source=ugentools.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_clip = ugentools.PV_MagClip(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_mag_clip.threshold
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]
