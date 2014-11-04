# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.ChaosGen import ChaosGen


class LorenzL(ChaosGen):

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
        b=2.667,
        frequency=22050,
        h=0.05,
        r=28,
        s=10,
        xi=0.1,
        yi=0,
        zi=0,
        ):
        ChaosGen.__init__(
            self,
            calculation_rate=calculation_rate,
            b=b,
            frequency=frequency,
            h=h,
            r=r,
            s=s,
            xi=xi,
            yi=yi,
            zi=zi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        b=2.667,
        frequency=22050,
        h=0.05,
        r=28,
        s=10,
        xi=0.1,
        yi=0,
        zi=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            b=b,
            frequency=frequency,
            h=h,
            r=r,
            s=s,
            xi=xi,
            yi=yi,
            zi=zi,
            )
        return ugen

    # def equation(): ...
