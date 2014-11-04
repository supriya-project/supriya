# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InBus(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
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
        from supriya.tools import synthdeftools
        calculation_rate = None
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
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            clip=clip,
            offset=offset,
            )
        return ugen

    # def new1(): ...
