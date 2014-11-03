# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.DUGen import DUGen


class Dseries(DUGen):

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
        length="float('inf')",
        start=1,
        step=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            length=length,
            start=start,
            step=step,
            )
        return ugen
