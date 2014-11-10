# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.ChaosGen import ChaosGen


class HenonN(ChaosGen):

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
        a=1.4,
        b=0.3,
        frequency=22050,
        x_0=0,
        x_1=0,
        ):
        ChaosGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            frequency=frequency,
            x_0=x_0,
            x_1=x_1,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.4,
        b=0.3,
        frequency=22050,
        x_0=0,
        x_1=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            frequency=frequency,
            x_0=x_0,
            x_1=x_1,
            )
        return ugen

    # def equation(): ...
