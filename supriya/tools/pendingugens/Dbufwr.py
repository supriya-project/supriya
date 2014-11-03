# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.DUGen import DUGen


class Dbufwr(DUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        bufnum=0,
        input=0,
        loop=1,
        phase=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            input=input,
            loop=loop,
            phase=phase,
            )
        return ugen
