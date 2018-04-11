from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_BinScramble(PV_ChainUGen):
    """
    Scrambles bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_bin_scramble = supriya.ugens.PV_BinScramble(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ...     )
        >>> pv_bin_scramble
        PV_BinScramble.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'wipe',
        'width',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        """
        Constructs a PV_BinScramble.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_scramble = supriya.ugens.PV_BinScramble.new(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble
            PV_BinScramble.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_BinScramble.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_scramble = supriya.ugens.PV_BinScramble(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of PV_BinScramble.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_scramble = supriya.ugens.PV_BinScramble(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def width(self):
        """
        Gets `width` input of PV_BinScramble.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_scramble = supriya.ugens.PV_BinScramble(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.width
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]

    @property
    def wipe(self):
        """
        Gets `wipe` input of PV_BinScramble.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_bin_scramble = supriya.ugens.PV_BinScramble(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.wipe
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]
