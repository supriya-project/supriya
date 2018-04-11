from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class FFT(PV_ChainUGen):
    """
    A fast Fourier transform.

    ::

        >>> buffer_id = supriya.ugens.LocalBuf(2048)
        >>> source = supriya.ugens.SoundIn.ar(bus=0)
        >>> fft = supriya.ugens.FFT(
        ...     active=1,
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     source=source,
        ...     window_size=0,
        ...     window_type=0,
        ...     )
        >>> fft
        FFT.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'hop',
        'window_type',
        'active',
        'window_size',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        source=None,
        active=1,
        hop=0.5,
        window_size=0,
        window_type=0,
        ):
        import supriya.ugens
        if buffer_id is None:
            buffer_size = window_size or 2048
            buffer_id = supriya.ugens.LocalBuf(buffer_size)
        PV_ChainUGen.__init__(
            self,
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        active=1,
        buffer_id=None,
        hop=0.5,
        source=None,
        window_size=0,
        window_type=0,
        ):
        """
        Constructs a FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT.new(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft
            FFT.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def active(self):
        """
        Gets `active` input of FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.active
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('active')
        return self._inputs[index]

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.buffer_id
            LocalBuf.ir()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def fft_size(self):
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        import supriya.ugens
        return supriya.ugens.BufFrames.ir(self.buffer_id)

    @property
    def hop(self):
        """
        Gets `hop` input of FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.hop
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('hop')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def window_size(self):
        """
        Gets `window_size` input of FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.window_size
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]

    @property
    def window_type(self):
        """
        Gets `window_type` input of FFT.

        ::

            >>> buffer_id = supriya.ugens.LocalBuf(2048)
            >>> source = supriya.ugens.SoundIn.ar(bus=0)
            >>> fft = supriya.ugens.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.window_type
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_type')
        return self._inputs[index]
