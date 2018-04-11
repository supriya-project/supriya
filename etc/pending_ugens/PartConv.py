from supriya.ugens.UGen import UGen


class PartConv(UGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> part_conv = supriya.ugens.PartConv.ar(
        ...     fftsize=fftsize,
        ...     irbufnum=irbufnum,
        ...     source=source,
        ...     )
        >>> part_conv
        PartConv.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'fftsize',
        'irbufnum',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        fftsize=None,
        irbufnum=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            fftsize=fftsize,
            irbufnum=irbufnum,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        fftsize=None,
        irbufnum=None,
        source=None,
        ):
        """
        Constructs an audio-rate PartConv.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> part_conv = supriya.ugens.PartConv.ar(
            ...     fftsize=fftsize,
            ...     irbufnum=irbufnum,
            ...     source=source,
            ...     )
            >>> part_conv
            PartConv.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            fftsize=fftsize,
            irbufnum=irbufnum,
            source=source,
            )
        return ugen

    # def calcBufSize(): ...

    # def calcNumPartitions(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def fftsize(self):
        """
        Gets `fftsize` input of PartConv.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> part_conv = supriya.ugens.PartConv.ar(
            ...     fftsize=fftsize,
            ...     irbufnum=irbufnum,
            ...     source=source,
            ...     )
            >>> part_conv.fftsize

        Returns ugen input.
        """
        index = self._ordered_input_names.index('fftsize')
        return self._inputs[index]

    @property
    def irbufnum(self):
        """
        Gets `irbufnum` input of PartConv.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> part_conv = supriya.ugens.PartConv.ar(
            ...     fftsize=fftsize,
            ...     irbufnum=irbufnum,
            ...     source=source,
            ...     )
            >>> part_conv.irbufnum

        Returns ugen input.
        """
        index = self._ordered_input_names.index('irbufnum')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of PartConv.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> part_conv = supriya.ugens.PartConv.ar(
            ...     fftsize=fftsize,
            ...     irbufnum=irbufnum,
            ...     source=source,
            ...     )
            >>> part_conv.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
