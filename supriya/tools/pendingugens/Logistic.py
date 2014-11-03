# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Logistic(UGen):

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
        chaos_param=3,
        frequency=1000,
        init=0.5,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chaos_param=chaos_param,
            frequency=frequency,
            init=init,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        chaos_param=3,
        frequency=1000,
        init=0.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_param=chaos_param,
            frequency=frequency,
            init=init,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        chaos_param=3,
        frequency=1000,
        init=0.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_param=chaos_param,
            frequency=frequency,
            init=init,
            )
        return ugen
