# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

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
