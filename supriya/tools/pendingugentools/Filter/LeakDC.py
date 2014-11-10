# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class LeakDC(Filter):

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
        coef=0.995,
        source=0,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            coef=coef,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coef=0.995,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coef=coef,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        coef=0.9,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coef=coef,
            source=source,
            )
        return ugen
