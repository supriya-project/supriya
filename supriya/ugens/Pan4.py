from supriya.ugens.MultiOutUGen import MultiOutUGen


class Pan4(MultiOutUGen):
    """
    A four-channel equal-power panner.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> pan_4 = supriya.ugens.Pan4.ar(
        ...     gain=1,
        ...     source=source,
        ...     x_position=0,
        ...     y_position=0,
        ...     )
        >>> pan_4
        UGenArray({4})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'x_position',
        'y_position',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        gain=1,
        source=None,
        x_position=0,
        y_position=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=4,
            gain=gain,
            source=source,
            x_position=x_position,
            y_position=y_position,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        gain=1,
        source=None,
        x_position=0,
        y_position=0,
        ):
        """
        Constructs an audio-rate Pan4.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pan_4 = supriya.ugens.Pan4.ar(
            ...     gain=1,
            ...     source=source,
            ...     x_position=0,
            ...     y_position=0,
            ...     )
            >>> pan_4
            UGenArray({4})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            gain=gain,
            source=source,
            x_position=x_position,
            y_position=y_position,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        gain=1,
        source=None,
        x_position=0,
        y_position=0,
        ):
        """
        Constructs a control-rate Pan4.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pan_4 = supriya.ugens.Pan4.kr(
            ...     gain=1,
            ...     source=source,
            ...     x_position=0,
            ...     y_position=0,
            ...     )
            >>> pan_4
            UGenArray({4})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            gain=gain,
            source=source,
            x_position=x_position,
            y_position=y_position,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def gain(self):
        """
        Gets `gain` input of Pan4.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pan_4 = supriya.ugens.Pan4.ar(
            ...     gain=1,
            ...     source=source,
            ...     x_position=0,
            ...     y_position=0,
            ...     )
            >>> pan_4[0].source.gain
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Pan4.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pan_4 = supriya.ugens.Pan4.ar(
            ...     gain=1,
            ...     source=source,
            ...     x_position=0,
            ...     y_position=0,
            ...     )
            >>> pan_4[0].source.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def x_position(self):
        """
        Gets `x_position` input of Pan4.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pan_4 = supriya.ugens.Pan4.ar(
            ...     gain=1,
            ...     source=source,
            ...     x_position=0,
            ...     y_position=0,
            ...     )
            >>> pan_4[0].source.x_position
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('x_position')
        return self._inputs[index]

    @property
    def y_position(self):
        """
        Gets `y_position` input of Pan4.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> pan_4 = supriya.ugens.Pan4.ar(
            ...     gain=1,
            ...     source=source,
            ...     x_position=0,
            ...     y_position=0,
            ...     )
            >>> pan_4[0].source.y_position
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('y_position')
        return self._inputs[index]
