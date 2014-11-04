# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Phasor(UGen):

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
        end=1,
        rate=1,
        reset_pos=0,
        start=0,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            end=end,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        end=1,
        rate=1,
        reset_pos=0,
        start=0,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            end=end,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        end=1,
        rate=1,
        reset_pos=0,
        start=0,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            end=end,
            rate=rate,
            reset_pos=reset_pos,
            start=start,
            trigger=trigger,
            )
        return ugen
