# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Gendy1(UGen):

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
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        init_cps=12,
        knum=None,
        maxfrequency=660,
        minfrequency=440,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            init_cps=init_cps,
            knum=knum,
            maxfrequency=maxfrequency,
            minfrequency=minfrequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        init_cps=12,
        knum=None,
        maxfrequency=660,
        minfrequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            init_cps=init_cps,
            knum=knum,
            maxfrequency=maxfrequency,
            minfrequency=minfrequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        adparam=1,
        ampdist=1,
        ampscale=0.5,
        ddparam=1,
        durdist=1,
        durscale=0.5,
        init_cps=12,
        knum=None,
        maxfrequency=1000,
        minfrequency=20,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            adparam=adparam,
            ampdist=ampdist,
            ampscale=ampscale,
            ddparam=ddparam,
            durdist=durdist,
            durscale=durscale,
            init_cps=init_cps,
            knum=knum,
            maxfrequency=maxfrequency,
            minfrequency=minfrequency,
            )
        return ugen
