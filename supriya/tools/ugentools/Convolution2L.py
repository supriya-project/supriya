# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Convolution2L(UGen):
    r'''Strict convolution with fixed kernel which can be updated using a trigger signal.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> kernel = ugentools.Mix.new(
        ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
        ...     ugentools.MouseX.kr(minimum=1, maximum=2),
        ...     )
        >>> convolution_2_l = ugentools.Convolution2L.ar(
        ...     crossfade=1,
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> convolution_2_l
        Convolution2L.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'kernel',
        'trigger',
        'framesize',
        'crossfade',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        crossfade=1,
        framesize=2048,
        kernel=None,
        source=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel=kernel,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        crossfade=1,
        framesize=2048,
        kernel=None,
        source=None,
        trigger=0,
        ):
        r'''Constructs an audio-rate Convolution2L.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution_2_l = ugentools.Convolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel=kernel,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> convolution_2_l
            Convolution2L.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel=kernel,
            source=source,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def crossfade(self):
        r'''Gets `crossfade` input of Convolution2L.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution_2_l = ugentools.Convolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel=kernel,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> convolution_2_l.crossfade
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('crossfade')
        return self._inputs[index]

    @property
    def framesize(self):
        r'''Gets `framesize` input of Convolution2L.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution_2_l = ugentools.Convolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel=kernel,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> convolution_2_l.framesize
            2048.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('framesize')
        return self._inputs[index]

    @property
    def kernel(self):
        r'''Gets `kernel` input of Convolution2L.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution_2_l = ugentools.Convolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel=kernel,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> convolution_2_l.kernel
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
        '''
        index = self._ordered_input_names.index('kernel')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Convolution2L.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution_2_l = ugentools.Convolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel=kernel,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> convolution_2_l.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Convolution2L.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> kernel = ugentools.Mix.new(
            ...     ugentools.LFSaw.ar(frequency=[300, 500, 800, 1000]) *
            ...     ugentools.MouseX.kr(minimum=1, maximum=2),
            ...     )
            >>> convolution_2_l = ugentools.Convolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel=kernel,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> convolution_2_l.trigger
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]