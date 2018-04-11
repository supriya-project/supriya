from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PackFFT(PV_ChainUGen):
    """

    ::

        >>> pack_fft = supriya.ugens.PackFFT.ar(
        ...     bufsize=bufsize,
        ...     chain=chain,
        ...     frombin=0,
        ...     magsphases=magsphases,
        ...     tobin=tobin,
        ...     zeroothers=0,
        ...     )
        >>> pack_fft
        PackFFT.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'chain',
        'bufsize',
        'magsphases',
        'frombin',
        'tobin',
        'zeroothers',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bufsize=None,
        chain=None,
        frombin=0,
        magsphases=None,
        tobin=None,
        zeroothers=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufsize=bufsize,
            chain=chain,
            frombin=frombin,
            magsphases=magsphases,
            tobin=tobin,
            zeroothers=zeroothers,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        bufsize=None,
        chain=None,
        frombin=0,
        magsphases=None,
        tobin=None,
        zeroothers=0,
        ):
        """
        Constructs a PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.new(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft
            PackFFT.new()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufsize=bufsize,
            chain=chain,
            frombin=frombin,
            magsphases=magsphases,
            tobin=tobin,
            zeroothers=zeroothers,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bufsize(self):
        """
        Gets `bufsize` input of PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft.bufsize

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bufsize')
        return self._inputs[index]

    @property
    def chain(self):
        """
        Gets `chain` input of PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft.chain

        Returns ugen input.
        """
        index = self._ordered_input_names.index('chain')
        return self._inputs[index]

    @property
    def frombin(self):
        """
        Gets `frombin` input of PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft.frombin
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frombin')
        return self._inputs[index]

    @property
    def magsphases(self):
        """
        Gets `magsphases` input of PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft.magsphases

        Returns ugen input.
        """
        index = self._ordered_input_names.index('magsphases')
        return self._inputs[index]

    @property
    def tobin(self):
        """
        Gets `tobin` input of PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft.tobin

        Returns ugen input.
        """
        index = self._ordered_input_names.index('tobin')
        return self._inputs[index]

    @property
    def zeroothers(self):
        """
        Gets `zeroothers` input of PackFFT.

        ::

            >>> pack_fft = supriya.ugens.PackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     magsphases=magsphases,
            ...     tobin=tobin,
            ...     zeroothers=0,
            ...     )
            >>> pack_fft.zeroothers
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('zeroothers')
        return self._inputs[index]
