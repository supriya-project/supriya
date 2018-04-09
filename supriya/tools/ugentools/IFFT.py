from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class IFFT(WidthFirstUGen):
    """
    An inverse fast Fourier transform.

    ::

        >>> pv_chain = ugentools.LocalBuf(2048)
        >>> ifft = ugentools.IFFT.ar(
        ...     pv_chain=pv_chain,
        ...     window_size=0,
        ...     window_type=0,
        ...     )
        >>> ifft
        IFFT.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'window_type',
        'window_size',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        calculation_rate=None,
        window_size=0,
        window_type=0,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            window_size=window_size,
            window_type=window_type,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        pv_chain=None,
        window_size=0,
        window_type=0,
        ):
        """
        Constructs an audio-rate IFFT.

        ::

            >>> pv_chain = ugentools.LocalBuf(2048)
            >>> ifft = ugentools.IFFT.ar(
            ...     pv_chain=pv_chain,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> ifft
            IFFT.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            window_size=window_size,
            window_type=window_type,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        pv_chain=None,
        window_size=0,
        window_type=0,
        ):
        """
        Constructs a control-rate IFFT.

        ::

            >>> pv_chain = ugentools.LocalBuf(2048)
            >>> ifft = ugentools.IFFT.kr(
            ...     pv_chain=pv_chain,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> ifft
            IFFT.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pv_chain=pv_chain,
            window_size=window_size,
            window_type=window_type,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of IFFT.

        ::

            >>> pv_chain = ugentools.LocalBuf(2048)
            >>> ifft = ugentools.IFFT.ar(
            ...     pv_chain=pv_chain,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> ifft.pv_chain
            LocalBuf.ir()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def window_size(self):
        """
        Gets `window_size` input of IFFT.

        ::

            >>> pv_chain = ugentools.LocalBuf(2048)
            >>> ifft = ugentools.IFFT.ar(
            ...     pv_chain=pv_chain,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> ifft.window_size
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]

    @property
    def window_type(self):
        """
        Gets `window_type` input of IFFT.

        ::

            >>> pv_chain = ugentools.LocalBuf(2048)
            >>> ifft = ugentools.IFFT.ar(
            ...     pv_chain=pv_chain,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> ifft.window_type
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('window_type')
        return self._inputs[index]
