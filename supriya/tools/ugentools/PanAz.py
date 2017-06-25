from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanAz(MultiOutUGen):
    """
    A multi-channel equal-power panner.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> pan_az = ugentools.PanAz.ar(
        ...     channel_count=8,
        ...     gain=1,
        ...     orientation=0.5,
        ...     position=0,
        ...     source=source,
        ...     width=2,
        ...     )
        >>> pan_az
        UGenArray({8})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'channel_count',
        'source',
        'position',
        'gain',
        'width',
        'orientation',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=8,
        gain=1,
        orientation=0.5,
        position=0,
        source=None,
        width=2,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            gain=gain,
            orientation=orientation,
            position=position,
            source=source,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=None,
        gain=1,
        orientation=0.5,
        position=0,
        source=None,
        width=2,
        ):
        """
        Constructs an audio-rate PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az
            UGenArray({8})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            gain=gain,
            orientation=orientation,
            position=position,
            source=source,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channel_count=None,
        gain=1,
        orientation=0.5,
        position=0,
        source=None,
        width=2,
        ):
        """
        Constructs a control-rate PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.kr(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az
            UGenArray({8})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            gain=gain,
            orientation=orientation,
            position=position,
            source=source,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az[0].source.channel_count
            8

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return int(self._inputs[index])

    @property
    def gain(self):
        """
        Gets `gain` input of PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az[0].source.gain
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def orientation(self):
        """
        Gets `orientation` input of PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az[0].source.orientation
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('orientation')
        return self._inputs[index]

    @property
    def position(self):
        """
        Gets `position` input of PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az[0].source.position
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az[0].source.source
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

    @property
    def width(self):
        """
        Gets `width` input of PanAz.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_az = ugentools.PanAz.ar(
            ...     channel_count=8,
            ...     gain=1,
            ...     orientation=0.5,
            ...     position=0,
            ...     source=source,
            ...     width=2,
            ...     )
            >>> pan_az[0].source.width
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]
