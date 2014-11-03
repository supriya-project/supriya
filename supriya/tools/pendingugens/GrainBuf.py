# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainBuf(MultiOutUGen):

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
        interp=2,
        max_grains=512,
        pan=0,
        pos=0,
        rate=1,
        sndbuf=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            interp=interp,
            max_grains=max_grains,
            pan=pan,
            pos=pos,
            rate=rate,
            sndbuf=sndbuf,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        interp=2,
        max_grains=512,
        pan=0,
        pos=0,
        rate=1,
        sndbuf=None,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            interp=interp,
            max_grains=max_grains,
            pan=pan,
            pos=pos,
            rate=rate,
            sndbuf=sndbuf,
            trigger=trigger,
            )
        return ugen
