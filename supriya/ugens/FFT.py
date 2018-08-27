import collections
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

    _ordered_input_names = collections.OrderedDict([
        ('buffer_id', None),
        ('source', None),
        ('hop', 0.5),
        ('window_type', 0),
        ('active', 1),
        ('window_size', 0),
    ])

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

    ### PUBLIC PROPERTIES ###

    @property
    def fft_size(self):
        """
        Gets FFT size as UGen input.

        Returns ugen input.
        """
        import supriya.ugens
        return supriya.ugens.BufFrames.ir(self.buffer_id)
