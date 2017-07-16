from supriya.tools.ugentools.UGen import UGen


class Convolution(UGen):
    """
    A real-time convolver.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> kernel = ugentools.Mix.new(
        ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
        ...     ugentools.MouseX.kr(minimum=1, maximum=2),
        ...     )
        >>> convolution = ugentools.Convolution.ar(
        ...     framesize=512,
        ...     kernel=kernel,
        ...     source=source,
        ...     )
        >>> convolution
        Convolution.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'kernel',
        'framesize',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        framesize=512,
        kernel=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            framesize=framesize,
            kernel=kernel,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        framesize=512,
        kernel=None,
        source=None,
        ):
        """
        Constructs an audio-rate Convolution.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=kernel,
            ...     source=source,
            ...     )
            >>> convolution
            Convolution.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            framesize=framesize,
            kernel=kernel,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def framesize(self):
        """
        Gets `framesize` input of Convolution.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=kernel,
            ...     source=source,
            ...     )
            >>> convolution.framesize
            512

        Returns ugen input.
        """
        index = self._ordered_input_names.index('framesize')
        return int(self._inputs[index])

    @property
    def kernel(self):
        """
        Gets `kernel` input of Convolution.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=kernel,
            ...     source=source,
            ...     )
            >>> convolution.kernel
            OutputProxy(
                source=Sum4(
                    input_one=OutputProxy(
                        source=BinaryOpUGen(
                            left=OutputProxy(
                                source=LFSaw(
                                    calculation_rate=CalculationRate.AUDIO,
                                    frequency=300.0,
                                    initial_phase=0.0
                                    ),
                                output_index=0
                                ),
                            right=OutputProxy(
                                source=MouseX(
                                    calculation_rate=CalculationRate.CONTROL,
                                    lag=0.2,
                                    maximum=2.0,
                                    minimum=1.0,
                                    warp=0.0
                                    ),
                                output_index=0
                                ),
                            calculation_rate=CalculationRate.AUDIO,
                            special_index=2
                            ),
                        output_index=0
                        ),
                    input_two=OutputProxy(
                        source=BinaryOpUGen(
                            left=OutputProxy(
                                source=LFSaw(
                                    calculation_rate=CalculationRate.AUDIO,
                                    frequency=500.0,
                                    initial_phase=0.0
                                    ),
                                output_index=0
                                ),
                            right=OutputProxy(
                                source=MouseX(
                                    calculation_rate=CalculationRate.CONTROL,
                                    lag=0.2,
                                    maximum=2.0,
                                    minimum=1.0,
                                    warp=0.0
                                    ),
                                output_index=0
                                ),
                            calculation_rate=CalculationRate.AUDIO,
                            special_index=2
                            ),
                        output_index=0
                        ),
                    input_three=OutputProxy(
                        source=BinaryOpUGen(
                            left=OutputProxy(
                                source=LFSaw(
                                    calculation_rate=CalculationRate.AUDIO,
                                    frequency=800.0,
                                    initial_phase=0.0
                                    ),
                                output_index=0
                                ),
                            right=OutputProxy(
                                source=MouseX(
                                    calculation_rate=CalculationRate.CONTROL,
                                    lag=0.2,
                                    maximum=2.0,
                                    minimum=1.0,
                                    warp=0.0
                                    ),
                                output_index=0
                                ),
                            calculation_rate=CalculationRate.AUDIO,
                            special_index=2
                            ),
                        output_index=0
                        ),
                    input_four=OutputProxy(
                        source=BinaryOpUGen(
                            left=OutputProxy(
                                source=LFSaw(
                                    calculation_rate=CalculationRate.AUDIO,
                                    frequency=1000.0,
                                    initial_phase=0.0
                                    ),
                                output_index=0
                                ),
                            right=OutputProxy(
                                source=MouseX(
                                    calculation_rate=CalculationRate.CONTROL,
                                    lag=0.2,
                                    maximum=2.0,
                                    minimum=1.0,
                                    warp=0.0
                                    ),
                                output_index=0
                                ),
                            calculation_rate=CalculationRate.AUDIO,
                            special_index=2
                            ),
                        output_index=0
                        )
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('kernel')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Convolution.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=kernel,
            ...     source=source,
            ...     )
            >>> convolution.source
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
