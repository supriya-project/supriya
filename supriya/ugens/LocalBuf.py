from supriya.synthdefs.CalculationRate import CalculationRate
from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class LocalBuf(WidthFirstUGen):
    """
    A synth-local buffer.

    ::

        >>> local_buf = supriya.ugens.LocalBuf(
        ...     channel_count=1,
        ...     frame_count=1,
        ...     )
        >>> local_buf
        LocalBuf.ir()

    LocalBuf creates a MaxLocalBuf UGen implicitly during SynthDef compilation.

    ::

        >>> with supriya.synthdefs.SynthDefBuilder() as builder:
        ...     local_buf = supriya.ugens.LocalBuf(2048)
        ...     source = supriya.ugens.PinkNoise.ar()
        ...     pv_chain = supriya.ugens.FFT(
        ...         buffer_id=local_buf,
        ...         source=source,
        ...         )
        ...     ifft = supriya.ugens.IFFT.ar(pv_chain=pv_chain)
        ...     out = supriya.ugens.Out.ar(bus=0, source=ifft)
        ...
        >>> synthdef = builder.build()
        >>> for ugen in synthdef.ugens:
        ...     ugen
        ...
        MaxLocalBufs.ir()
        LocalBuf.ir()
        PinkNoise.ar()
        FFT.kr()
        IFFT.ar()
        Out.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'frame_count',
        )

    _valid_calculation_rates = (
        CalculationRate.SCALAR,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        frame_count=1,
        channel_count=1,
        calculation_rate=None,
        ):
        import supriya.synthdefs
        if calculation_rate is None:
            calculation_rate = supriya.synthdefs.CalculationRate.SCALAR
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            frame_count=frame_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        channel_count=1,
        frame_count=1,
        ):
        """
        Constructs a LocalBuf.

        ::

            >>> local_buf = supriya.ugens.LocalBuf.new(
            ...     channel_count=1,
            ...     frame_count=1,
            ...     )
            >>> local_buf
            LocalBuf.ir()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            frame_count=frame_count,
            )
        return ugen

    # def new1(): ...

    # def newFrom(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of LocalBuf.

        ::

            >>> local_buf = supriya.ugens.LocalBuf(
            ...     channel_count=2,
            ...     frame_count=1,
            ...     )
            >>> local_buf.channel_count
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def frame_count(self):
        """
        Gets `frame_count` input of LocalBuf.

        ::

            >>> local_buf = supriya.ugens.LocalBuf(
            ...     channel_count=2,
            ...     frame_count=1,
            ...     )
            >>> local_buf.frame_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frame_count')
        return self._inputs[index]
