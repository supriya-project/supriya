import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import MultiOutUGen


class UnpackFFT(MultiOutUGen):
    """

    ::

        >>> unpack_fft = supriya.ugens.UnpackFFT.ar(
        ...     bufsize=bufsize,
        ...     chain=chain,
        ...     frombin=0,
        ...     tobin=tobin,
        ...     )
        >>> unpack_fft
        UnpackFFT.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = collections.OrderedDict(
        'chain',
        'bufsize',
        'frombin',
        'tobin',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bufsize=None,
        chain=None,
        frombin=0,
        tobin=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufsize=bufsize,
            chain=chain,
            frombin=frombin,
            tobin=tobin,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        bufsize=None,
        chain=None,
        frombin=0,
        tobin=None,
        ):
        """
        Constructs a UnpackFFT.

        ::

            >>> unpack_fft = supriya.ugens.UnpackFFT.new(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     tobin=tobin,
            ...     )
            >>> unpack_fft
            UnpackFFT.new()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufsize=bufsize,
            chain=chain,
            frombin=frombin,
            tobin=tobin,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bufsize(self):
        """
        Gets `bufsize` input of UnpackFFT.

        ::

            >>> unpack_fft = supriya.ugens.UnpackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     tobin=tobin,
            ...     )
            >>> unpack_fft.bufsize

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bufsize')
        return self._inputs[index]

    @property
    def chain(self):
        """
        Gets `chain` input of UnpackFFT.

        ::

            >>> unpack_fft = supriya.ugens.UnpackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     tobin=tobin,
            ...     )
            >>> unpack_fft.chain

        Returns ugen input.
        """
        index = self._ordered_input_names.index('chain')
        return self._inputs[index]

    @property
    def frombin(self):
        """
        Gets `frombin` input of UnpackFFT.

        ::

            >>> unpack_fft = supriya.ugens.UnpackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     tobin=tobin,
            ...     )
            >>> unpack_fft.frombin
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frombin')
        return self._inputs[index]

    @property
    def tobin(self):
        """
        Gets `tobin` input of UnpackFFT.

        ::

            >>> unpack_fft = supriya.ugens.UnpackFFT.ar(
            ...     bufsize=bufsize,
            ...     chain=chain,
            ...     frombin=0,
            ...     tobin=tobin,
            ...     )
            >>> unpack_fft.tobin

        Returns ugen input.
        """
        index = self._ordered_input_names.index('tobin')
        return self._inputs[index]
