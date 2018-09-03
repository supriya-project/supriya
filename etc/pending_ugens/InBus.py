import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class InBus(UGen):
    """

    ::

        >>> in_bus = supriya.ugens.InBus.ar(
        ...     bus=bus,
        ...     channel_count=channel_count,
        ...     clip=clip,
        ...     offset=0,
        ...     )
        >>> in_bus
        InBus.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'bus',
        'channel_count',
        'offset',
        'clip',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=None,
        channel_count=None,
        clip=None,
        offset=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            clip=clip,
            offset=offset,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=None,
        channel_count=None,
        clip=None,
        offset=0,
        ):
        """
        Constructs an audio-rate InBus.

        ::

            >>> in_bus = supriya.ugens.InBus.ar(
            ...     bus=bus,
            ...     channel_count=channel_count,
            ...     clip=clip,
            ...     offset=0,
            ...     )
            >>> in_bus
            InBus.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            clip=clip,
            offset=offset,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=None,
        channel_count=None,
        clip=None,
        offset=0,
        ):
        """
        Constructs a control-rate InBus.

        ::

            >>> in_bus = supriya.ugens.InBus.kr(
            ...     bus=bus,
            ...     channel_count=channel_count,
            ...     clip=clip,
            ...     offset=0,
            ...     )
            >>> in_bus
            InBus.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            clip=clip,
            offset=offset,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of InBus.

        ::

            >>> in_bus = supriya.ugens.InBus.ar(
            ...     bus=bus,
            ...     channel_count=channel_count,
            ...     clip=clip,
            ...     offset=0,
            ...     )
            >>> in_bus.bus

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of InBus.

        ::

            >>> in_bus = supriya.ugens.InBus.ar(
            ...     bus=bus,
            ...     channel_count=channel_count,
            ...     clip=clip,
            ...     offset=0,
            ...     )
            >>> in_bus.channel_count

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def clip(self):
        """
        Gets `clip` input of InBus.

        ::

            >>> in_bus = supriya.ugens.InBus.ar(
            ...     bus=bus,
            ...     channel_count=channel_count,
            ...     clip=clip,
            ...     offset=0,
            ...     )
            >>> in_bus.clip

        Returns ugen input.
        """
        index = self._ordered_input_names.index('clip')
        return self._inputs[index]

    @property
    def offset(self):
        """
        Gets `offset` input of InBus.

        ::

            >>> in_bus = supriya.ugens.InBus.ar(
            ...     bus=bus,
            ...     channel_count=channel_count,
            ...     clip=clip,
            ...     offset=0,
            ...     )
            >>> in_bus.offset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]
