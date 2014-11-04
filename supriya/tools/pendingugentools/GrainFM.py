# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GrainFM(MultiOutUGen):

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
        carfrequency=440,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        index=1,
        max_grains=512,
        modfrequency=200,
        pan=0,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            carfrequency=carfrequency,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            index=index,
            max_grains=max_grains,
            modfrequency=modfrequency,
            pan=pan,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        carfrequency=440,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        index=1,
        max_grains=512,
        modfrequency=200,
        pan=0,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            carfrequency=carfrequency,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            index=index,
            max_grains=max_grains,
            modfrequency=modfrequency,
            pan=pan,
            trigger=trigger,
            )
        return ugen
