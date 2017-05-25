# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class DecodeB2(MultiOutUGen):
    """
    A 2D Ambisonic B-format decoder.

    ::

        >>> source = ugentools.PinkNoise.ar()
        >>> w, x, y = ugentools.PanB2.ar(
        ...     source=source,
        ...     azimuth=ugentools.SinOsc.kr(),
        ...     )
        >>> channel_count = 4
        >>> decode_b_2 = ugentools.DecodeB2.ar(
        ...     channel_count=channel_count,
        ...     orientation=0.5,
        ...     w=w,
        ...     x=x,
        ...     y=y,
        ...     )
        >>> decode_b_2
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        #'channel_count',
        'w',
        'x',
        'y',
        'orientation',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        """
        Constructs an audio-rate DecodeB2.

        ::

            >>> source = ugentools.PinkNoise.ar()
            >>> w, x, y = ugentools.PanB2.ar(
            ...     source=source,
            ...     azimuth=ugentools.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2
            UGenArray({4})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channel_count=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        """
        Constructs a control-rate DecodeB2.

        ::

            >>> source = ugentools.PinkNoise.ar()
            >>> w, x, y = ugentools.PanB2.ar(
            ...     source=source,
            ...     azimuth=ugentools.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = ugentools.DecodeB2.kr(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2
            UGenArray({4})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def orientation(self):
        """
        Gets `orientation` input of DecodeB2.

        ::

            >>> source = ugentools.PinkNoise.ar()
            >>> w, x, y = ugentools.PanB2.ar(
            ...     source=source,
            ...     azimuth=ugentools.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.orientation
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('orientation')
        return self._inputs[index]

    @property
    def w(self):
        """
        Gets `w` input of DecodeB2.

        ::

            >>> source = ugentools.PinkNoise.ar()
            >>> w, x, y = ugentools.PanB2.ar(
            ...     source=source,
            ...     azimuth=ugentools.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.w
            OutputProxy(
                source=PanB2(
                    calculation_rate=CalculationRate.AUDIO,
                    azimuth=OutputProxy(
                        source=SinOsc(
                            calculation_rate=CalculationRate.CONTROL,
                            frequency=440.0,
                            phase=0.0
                            ),
                        output_index=0
                        ),
                    gain=1.0,
                    source=OutputProxy(
                        source=PinkNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        )
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('w')
        return self._inputs[index]

    @property
    def x(self):
        """
        Gets `x` input of DecodeB2.

        ::

            >>> source = ugentools.PinkNoise.ar()
            >>> w, x, y = ugentools.PanB2.ar(
            ...     source=source,
            ...     azimuth=ugentools.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.x
            OutputProxy(
                source=PanB2(
                    calculation_rate=CalculationRate.AUDIO,
                    azimuth=OutputProxy(
                        source=SinOsc(
                            calculation_rate=CalculationRate.CONTROL,
                            frequency=440.0,
                            phase=0.0
                            ),
                        output_index=0
                        ),
                    gain=1.0,
                    source=OutputProxy(
                        source=PinkNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        )
                    ),
                output_index=1
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('x')
        return self._inputs[index]

    @property
    def y(self):
        """
        Gets `y` input of DecodeB2.

        ::

            >>> source = ugentools.PinkNoise.ar()
            >>> w, x, y = ugentools.PanB2.ar(
            ...     source=source,
            ...     azimuth=ugentools.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = ugentools.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.y
            OutputProxy(
                source=PanB2(
                    calculation_rate=CalculationRate.AUDIO,
                    azimuth=OutputProxy(
                        source=SinOsc(
                            calculation_rate=CalculationRate.CONTROL,
                            frequency=440.0,
                            phase=0.0
                            ),
                        output_index=0
                        ),
                    gain=1.0,
                    source=OutputProxy(
                        source=PinkNoise(
                            calculation_rate=CalculationRate.AUDIO
                            ),
                        output_index=0
                        )
                    ),
                output_index=2
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('y')
        return self._inputs[index]