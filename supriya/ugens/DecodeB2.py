from supriya.ugens.MultiOutUGen import MultiOutUGen


class DecodeB2(MultiOutUGen):
    """
    A 2D Ambisonic B-format decoder.

    ::

        >>> source = supriya.ugens.PinkNoise.ar()
        >>> w, x, y = supriya.ugens.PanB2.ar(
        ...     source=source,
        ...     azimuth=supriya.ugens.SinOsc.kr(),
        ...     )
        >>> channel_count = 4
        >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
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

            >>> source = supriya.ugens.PinkNoise.ar()
            >>> w, x, y = supriya.ugens.PanB2.ar(
            ...     source=source,
            ...     azimuth=supriya.ugens.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
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
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
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

            >>> source = supriya.ugens.PinkNoise.ar()
            >>> w, x, y = supriya.ugens.PanB2.ar(
            ...     source=source,
            ...     azimuth=supriya.ugens.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = supriya.ugens.DecodeB2.kr(
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
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
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

            >>> source = supriya.ugens.PinkNoise.ar()
            >>> w, x, y = supriya.ugens.PanB2.ar(
            ...     source=source,
            ...     azimuth=supriya.ugens.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
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

            >>> source = supriya.ugens.PinkNoise.ar()
            >>> w, x, y = supriya.ugens.PanB2.ar(
            ...     source=source,
            ...     azimuth=supriya.ugens.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.w
            PanB2.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('w')
        return self._inputs[index]

    @property
    def x(self):
        """
        Gets `x` input of DecodeB2.

        ::

            >>> source = supriya.ugens.PinkNoise.ar()
            >>> w, x, y = supriya.ugens.PanB2.ar(
            ...     source=source,
            ...     azimuth=supriya.ugens.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.x
            PanB2.ar()[1]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('x')
        return self._inputs[index]

    @property
    def y(self):
        """
        Gets `y` input of DecodeB2.

        ::

            >>> source = supriya.ugens.PinkNoise.ar()
            >>> w, x, y = supriya.ugens.PanB2.ar(
            ...     source=source,
            ...     azimuth=supriya.ugens.SinOsc.kr(),
            ...     )
            >>> channel_count = 4
            >>> decode_b_2 = supriya.ugens.DecodeB2.ar(
            ...     channel_count=channel_count,
            ...     orientation=0.5,
            ...     w=w,
            ...     x=x,
            ...     y=y,
            ...     )
            >>> decode_b_2[0].source.y
            PanB2.ar()[2]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('y')
        return self._inputs[index]
