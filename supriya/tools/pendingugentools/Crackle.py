# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Crackle(UGen):

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
        chaos_param=1.5,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chaos_param=chaos_param,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        chaos_param=1.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_param=chaos_param,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        chaos_param=1.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_param=chaos_param,
            )
        return ugen
