from supriya.tools.ugentools.UGen import UGen


class XFade2(UGen):
    """
    Two channel equal power crossfader.

    ::

        >>> xfade_3 = ugentools.XFade2.ar(
        ...     in_a=ugentools.Saw.ar(),
        ...     in_b=ugentools.SinOsc.ar(),
        ...     level=1,
        ...     pan=ugentools.LFTri.kr(frequency=0.1),
        ...     )
        >>> xfade_3
        XFade2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'in_a',
        'in_b',
        'pan',
        'level',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        """
        Constructs an audio-rate XFade2.

        ::

            >>> xfade_2 = ugentools.XFade2.ar(
            ...     in_a=ugentools.Saw.ar(),
            ...     in_b=ugentools.SinOsc.ar(),
            ...     level=1,
            ...     pan=ugentools.LFTri.kr(frequency=0.1),
            ...     )
            >>> xfade_2
            XFade2.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        """
        Constructs a control-rate XFade2.

        ::

            >>> xfade_2 = ugentools.XFade2.kr(
            ...     in_a=ugentools.Saw.ar(),
            ...     in_b=ugentools.SinOsc.ar(),
            ...     level=1,
            ...     pan=ugentools.LFTri.kr(frequency=0.1),
            ...     )
            >>> xfade_2
            XFade2.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def in_a(self):
        """
        Gets `in_a` input of XFade2.

        ::

            >>> xfade_2 = ugentools.XFade2.ar(
            ...     in_a=ugentools.Saw.ar(),
            ...     in_b=ugentools.SinOsc.ar(),
            ...     level=1,
            ...     pan=ugentools.LFTri.kr(frequency=0.1),
            ...     )
            >>> xfade_2.in_a
            OutputProxy(
                source=Saw(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('in_a')
        return self._inputs[index]

    @property
    def in_b(self):
        """
        Gets `in_b` input of XFade2.

        ::

            >>> xfade_2 = ugentools.XFade2.ar(
            ...     in_a=ugentools.Saw.ar(),
            ...     in_b=ugentools.SinOsc.ar(),
            ...     level=1,
            ...     pan=ugentools.LFTri.kr(frequency=0.1),
            ...     )
            >>> xfade_2.in_b
            OutputProxy(
                source=SinOsc(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('in_b')
        return self._inputs[index]

    @property
    def level(self):
        """
        Gets `level` input of XFade2.

        ::

            >>> xfade_2 = ugentools.XFade2.ar(
            ...     in_a=ugentools.Saw.ar(),
            ...     in_b=ugentools.SinOsc.ar(),
            ...     level=1,
            ...     pan=ugentools.LFTri.kr(frequency=0.1),
            ...     )
            >>> xfade_2.level
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def pan(self):
        """
        Gets `pan` input of XFade2.

        ::

            >>> xfade_2 = ugentools.XFade2.ar(
            ...     in_a=ugentools.Saw.ar(),
            ...     in_b=ugentools.SinOsc.ar(),
            ...     level=1,
            ...     pan=ugentools.LFTri.kr(frequency=0.1),
            ...     )
            >>> xfade_2.pan
            OutputProxy(
                source=LFTri(
                    calculation_rate=CalculationRate.CONTROL,
                    frequency=0.1,
                    initial_phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]
