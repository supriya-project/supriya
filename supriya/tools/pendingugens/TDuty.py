# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.Duty import Duty


class TDuty(Duty):

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
        done_action=0,
        duration=1,
        gap_first=0,
        level=1,
        reset=0,
        ):
        Duty.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            gap_first=gap_first,
            level=level,
            reset=reset,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        duration=1,
        gap_first=0,
        level=1,
        reset=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            gap_first=gap_first,
            level=level,
            reset=reset,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        done_action=0,
        duration=1,
        gap_first=0,
        level=1,
        reset=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            gap_first=gap_first,
            level=level,
            reset=reset,
            )
        return ugen
