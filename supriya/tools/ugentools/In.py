# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):
    r'''A bus input unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.In.ar(bus=0, channel_count=4)
        UGenArray(
            (
                OutputProxy(
                    source=In(
                        bus=0.0,
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=0
                    ),
                OutputProxy(
                    source=In(
                        bus=0.0,
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=1
                    ),
                OutputProxy(
                    source=In(
                        bus=0.0,
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=2
                    ),
                OutputProxy(
                    source=In(
                        bus=0.0,
                        calculation_rate=<CalculationRate.AUDIO: 2>,
                        channel_count=4
                        ),
                    output_index=3
                    ),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('bus', 0),
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
        bus=None,
        channel_count=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new(
            calculation_rate=calculation_rate,
            special_index=0,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bus=None,
        channel_count=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new(
            calculation_rate=calculation_rate,
            special_index=0,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen
