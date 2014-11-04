# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.ChaosGen import ChaosGen


class FBSineN(ChaosGen):

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
        c=0.5,
        fb=0.1,
        frequency=22050,
        im=1,
        xi=0.1,
        yi=0.1,
        ):
        ChaosGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            fb=fb,
            frequency=frequency,
            im=im,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=1.1,
        c=0.5,
        fb=0.1,
        frequency=22050,
        im=1,
        xi=0.1,
        yi=0.1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            c=c,
            fb=fb,
            frequency=frequency,
            im=im,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...
