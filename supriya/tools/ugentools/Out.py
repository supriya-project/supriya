import collections
from supriya.tools.ugentools.UGen import UGen


class Out(UGen):
    """
    A bus output unit generator.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.Out.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        Out.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        UGen.__init__(
            self,
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        source=None,
        ):
        """
        Constructs an audio-rate bus output.

        ::

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> out = ugentools.Out.ar(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> out
            Out.ar()

        Returns ugen graph.
        """
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            bus = int(bus)
        ugen = cls._new_expanded(
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=0,
        source=None,
        ):
        """
        Constructs a control-rate bus output.

        ::

            >>> source = ugentools.SinOsc.kr(frequency=[4, 2])
            >>> out = ugentools.Out.kr(
            ...     bus=0,
            ...     source=source,
            ...     )
            >>> out
            Out.kr()

        Returns ugen graph.
        """
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            bus = int(bus)
        ugen = cls._new_expanded(
            bus=bus,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of Out.

        ::

            >>> bus = 0
            >>> source = ugentools.WhiteNoise.ar()
            >>> out = ugentools.Out.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> out.bus
            0.0

        Returns input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def is_output_ugen(self):
        return True

    @property
    def source(self):
        """
        Gets `source` input of Out.

        ::

            >>> bus = 0
            >>> source = ugentools.WhiteNoise.ar()
            >>> out = ugentools.Out.ar(
            ...     bus=bus,
            ...     source=source,
            ...     )
            >>> out.source
            (OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.AUDIO
                    ),
                output_index=0
                ),)

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
