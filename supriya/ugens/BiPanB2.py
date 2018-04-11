from supriya.ugens.MultiOutUGen import MultiOutUGen


class BiPanB2(MultiOutUGen):
    """
    A 2D ambisonic b-format panner.

    ::

        >>> in_a = supriya.ugens.SinOsc.ar()
        >>> in_b = supriya.ugens.WhiteNoise.ar()
        >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
        ...     azimuth=-0.5,
        ...     gain=1,
        ...     in_a=in_a,
        ...     in_b=in_b,
        ...     )
        >>> bi_pan_b_2
        UGenArray({3})

    ::

        >>> w, x, y = bi_pan_b_2

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'in_a',
        'in_b',
        'azimuth',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=3,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        """
        Constructs an audio-rate BiPanB2.

        ::

            >>> in_a = supriya.ugens.SinOsc.ar()
            >>> in_b = supriya.ugens.WhiteNoise.ar()
            >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
            ...     azimuth=-0.5,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2
            UGenArray({3})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        """
        Constructs a control-rate BiPanB2.

        ::

            >>> in_a = supriya.ugens.SinOsc.kr()
            >>> in_b = supriya.ugens.WhiteNoise.kr()
            >>> bi_pan_b_2 = supriya.ugens.BiPanB2.kr(
            ...     azimuth=-0.5,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2
            UGenArray({3})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def azimuth(self):
        """
        Gets `azimuth` input of BiPanB2.

        ::

            >>> in_a = supriya.ugens.SinOsc.ar()
            >>> in_b = supriya.ugens.WhiteNoise.ar()
            >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
            ...     azimuth=-0.5,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2[0].source.azimuth
            -0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('azimuth')
        return self._inputs[index]

    @property
    def gain(self):
        """
        Gets `gain` input of BiPanB2.

        ::

            >>> in_a = supriya.ugens.SinOsc.ar()
            >>> in_b = supriya.ugens.WhiteNoise.ar()
            >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
            ...     azimuth=-0.5,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2[0].source.gain
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def in_a(self):
        """
        Gets `in_a` input of BiPanB2.

        ::

            >>> in_a = supriya.ugens.SinOsc.ar()
            >>> in_b = supriya.ugens.WhiteNoise.ar()
            >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
            ...     azimuth=-0.5,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2[0].source.in_a
            SinOsc.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('in_a')
        return self._inputs[index]

    @property
    def in_b(self):
        """
        Gets `in_b` input of BiPanB2.

        ::

            >>> in_a = supriya.ugens.SinOsc.ar()
            >>> in_b = supriya.ugens.WhiteNoise.ar()
            >>> bi_pan_b_2 = supriya.ugens.BiPanB2.ar(
            ...     azimuth=-0.5,
            ...     gain=1,
            ...     in_a=in_a,
            ...     in_b=in_b,
            ...     )
            >>> bi_pan_b_2[0].source.in_b
            WhiteNoise.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('in_b')
        return self._inputs[index]
