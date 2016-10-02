# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):
    r'''A bus input unit generator.

    ::

        >>> ugentools.In.ar(bus=0, channel_count=4)
        UGenArray({4})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus=0,
        calculation_rate=None,
        channel_count=1,
        ):
        MultiOutUGen.__init__(
            self,
            bus=bus,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bus=0,
        channel_count=1,
        ):
        r'''Constructs an audio-rate bus input.

        ::

            >>> ugentools.In.ar(bus=0, channel_count=4)
            UGenArray({4})

        Returns ugen graph.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            if isinstance(bus, servertools.BusGroup):
                channel_count = len(bus)
            else:
                channel_count = 1
            bus = int(bus)
        ugen = cls._new_expanded(
            bus=bus,
            channel_count=channel_count,
            calculation_rate=calculation_rate,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        ):
        r'''Constructs a control-rate bus input.

        ::

            >>> ugentools.In.kr(bus=0, channel_count=4)
            UGenArray({4})

        Returns ugen graph.
        '''
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        prototype = (
            servertools.Bus,
            servertools.BusGroup,
            servertools.BusProxy,
            )
        if isinstance(bus, prototype):
            if isinstance(bus, servertools.BusGroup):
                channel_count = len(bus)
            else:
                channel_count = 1
            bus = int(bus)
        ugen = cls._new_expanded(
            bus=bus,
            channel_count=channel_count,
            calculation_rate=calculation_rate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r'''Gets `bus` input of DC.

        ::

            >>> bus = 2
            >>> in_ = ugentools.In.ar(
            ...     bus=bus,
            ...     )
            >>> in_.source.bus
            2.0

        Returns input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def is_input_ugen(self):
        return True
