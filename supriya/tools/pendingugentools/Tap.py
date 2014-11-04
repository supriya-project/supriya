# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Tap(UGen):

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
        bufnum=0,
        channel_count=1,
        delaytime=0.2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            delaytime=delaytime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=0,
        channel_count=1,
        delaytime=0.2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            delaytime=delaytime,
            )
        return ugen
