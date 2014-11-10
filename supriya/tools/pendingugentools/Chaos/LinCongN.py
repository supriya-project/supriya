# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.ChaosGen import ChaosGen


class LinCongN(ChaosGen):

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
        a=1.1,
        c=0.13,
        frequency=22050,
        m=1,
        xi=0,
        ):
        ChaosGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            frequency=frequency,
            m=m,
            xi=xi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.1,
        c=0.13,
        frequency=22050,
        m=1,
        xi=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            frequency=frequency,
            m=m,
            xi=xi,
            )
        return ugen

    # def equation(): ...
