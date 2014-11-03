# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class TGrains(MultiOutUGen):

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
        amp=0.1,
        bufnum=0,
        center_pos=0,
        channel_count=None,
        duration=0.1,
        interp=4,
        pan=0,
        rate=1,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp=amp,
            bufnum=bufnum,
            center_pos=center_pos,
            channel_count=channel_count,
            duration=duration,
            interp=interp,
            pan=pan,
            rate=rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        amp=0.1,
        bufnum=0,
        center_pos=0,
        channel_count=None,
        duration=0.1,
        interp=4,
        pan=0,
        rate=1,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            bufnum=bufnum,
            center_pos=center_pos,
            channel_count=channel_count,
            duration=duration,
            interp=interp,
            pan=pan,
            rate=rate,
            trigger=trigger,
            )
        return ugen
