from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_BrickWall(PV_ChainUGen):
    """
    Zeros bins.

    - If wipe == 0 then there is no effect.
    - If wipe > 0 then it acts like a high pass filter, clearing bins from the
      bottom up.
    - If wipe < 0 then it acts like a low pass filter, clearing bins from the
      top down.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_brick_wall = supriya.ugens.PV_BrickWall(
        ...     pv_chain=pv_chain,
        ...     wipe=0,
        ...     )
        >>> pv_brick_wall
        PV_BrickWall.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'wipe',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        wipe=0,
        ):
        """
        Constructs a PV_BrickWall.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_brick_wall = supriya.ugens.PV_BrickWall.new(
            ...     pv_chain=pv_chain,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall
            PV_BrickWall.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_BrickWall.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_brick_wall = supriya.ugens.PV_BrickWall(
            ...     pv_chain=pv_chain,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def wipe(self):
        """
        Gets `wipe` input of PV_BrickWall.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_brick_wall = supriya.ugens.PV_BrickWall(
            ...     pv_chain=pv_chain,
            ...     wipe=0,
            ...     )
            >>> pv_brick_wall.wipe
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]
