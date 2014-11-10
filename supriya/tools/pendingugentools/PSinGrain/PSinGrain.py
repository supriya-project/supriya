# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PSinGrain(UGen):

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
        amp=1,
        duration=0.2,
        frequency=440,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            amp=amp,
            duration=duration,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        amp=1,
        duration=0.2,
        frequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            duration=duration,
            frequency=frequency,
            )
        return ugen
