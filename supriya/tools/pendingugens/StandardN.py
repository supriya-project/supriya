# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.ChaosGen import ChaosGen


class StandardN(ChaosGen):

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
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        ChaosGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...
