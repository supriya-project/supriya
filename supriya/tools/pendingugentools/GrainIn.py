# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainIn(MultiOutUGen):

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
        channel_count=1,
        duration=1,
        envbufnum=-1,
        max_grains=512,
        pan=0,
        source=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            max_grains=max_grains,
            pan=pan,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        max_grains=512,
        pan=0,
        source=None,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            max_grains=max_grains,
            pan=pan,
            source=source,
            trigger=trigger,
            )
        return ugen
