from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_MagFreeze(PV_ChainUGen):
    """
    Freezes magnitudes.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze(
        ...     pv_chain=pv_chain,
        ...     freeze=0,
        ...     )
        >>> pv_mag_freeze
        PV_MagFreeze.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'freeze',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        freeze=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            freeze=freeze,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        freeze=0,
        ):
        """
        Constructs a PV_MagFreeze.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze.new(
            ...     pv_chain=pv_chain,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze
            PV_MagFreeze.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            freeze=freeze,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_MagFreeze.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze(
            ...     pv_chain=pv_chain,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def freeze(self):
        """
        Gets `freeze` input of PV_MagFreeze.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_mag_freeze = supriya.ugens.PV_MagFreeze(
            ...     pv_chain=pv_chain,
            ...     freeze=0,
            ...     )
            >>> pv_mag_freeze.freeze
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freeze')
        return self._inputs[index]
