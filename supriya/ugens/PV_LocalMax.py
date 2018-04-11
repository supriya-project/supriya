from supriya.ugens.PV_MagAbove import PV_MagAbove


class PV_LocalMax(PV_MagAbove):
    """
    Passes bins which are local maxima.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_local_max = supriya.ugens.PV_LocalMax(
        ...     pv_chain=pv_chain,
        ...     threshold=0,
        ...     )
        >>> pv_local_max
        PV_LocalMax.kr()

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
        Constructs a PV_LocalMax.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_local_max = supriya.ugens.PV_LocalMax.new(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_local_max
            PV_LocalMax.kr()

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
        Gets `pv_chain` input of PV_LocalMax.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_local_max = supriya.ugens.PV_LocalMax(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_local_max.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def threshold(self):
        """
        Gets `threshold` input of PV_LocalMax.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_local_max = supriya.ugens.PV_LocalMax(
            ...     pv_chain=pv_chain,
            ...     threshold=0,
            ...     )
            >>> pv_local_max.threshold
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]
