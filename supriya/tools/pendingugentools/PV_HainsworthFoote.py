# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.PV_ChainUGen import PV_ChainUGen


class PV_HainsworthFoote(PV_ChainUGen):

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
        buffer=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer=buffer,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer=None,
        propf=0,
        proph=0,
        threshold=1,
        waittime=0.04,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            propf=propf,
            proph=proph,
            threshold=threshold,
            waittime=waittime,
            )
        return ugen
