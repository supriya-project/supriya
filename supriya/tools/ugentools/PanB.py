# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanB(MultiOutUGen):
    """
    A 3D ambisonic b-format panner.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> pan_b = ugentools.PanB.ar(
        ...     azimuth=0,
        ...     elevation=0,
        ...     gain=1,
        ...     source=source,
        ...     )
        >>> pan_b
        UGenArray({3})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'azimuth',
        'elevation',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        azimuth=0,
        elevation=0,
        gain=1,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=3,
            azimuth=azimuth,
            elevation=elevation,
            gain=gain,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=0,
        elevation=0,
        gain=1,
        source=None,
        ):
        """
        Constructs an audio-rate PanB.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b
            UGenArray({3})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            elevation=elevation,
            gain=gain,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=0,
        elevation=0,
        gain=1,
        source=None,
        ):
        """
        Constructs a control-rate PanB.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b = ugentools.PanB.kr(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b
            UGenArray({3})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            elevation=elevation,
            gain=gain,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def azimuth(self):
        """
        Gets `azimuth` input of PanB.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b[0].source.azimuth
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('azimuth')
        return self._inputs[index]

    @property
    def elevation(self):
        """
        Gets `elevation` input of PanB.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b[0].source.elevation
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('elevation')
        return self._inputs[index]

    @property
    def gain(self):
        """
        Gets `gain` input of PanB.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b[0].source.gain
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of PanB.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b[0].source.source
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
