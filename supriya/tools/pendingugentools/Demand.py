# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Demand(MultiOutUGen):

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
        demand_ugens=None,
        reset=None,
        trigger=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            demand_ugens=demand_ugens,
            reset=reset,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        demand_ugens=None,
        reset=None,
        trigger=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            demand_ugens=demand_ugens,
            reset=reset,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        demand_ugens=None,
        reset=None,
        trigger=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            demand_ugens=demand_ugens,
            reset=reset,
            trigger=trigger,
            )
        return ugen
