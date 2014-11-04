# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.PV_ChainUGen import PV_ChainUGen


class PV_JensenAndersen(PV_ChainUGen):

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
        prophfc=0.25,
        prophfe=0.25,
        propsc=0.25,
        propsf=0.25,
        threshold=1,
        waittime=0.04,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer=buffer,
            prophfc=prophfc,
            prophfe=prophfe,
            propsc=propsc,
            propsf=propsf,
            threshold=threshold,
            waittime=waittime,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer=None,
        prophfc=0.25,
        prophfe=0.25,
        propsc=0.25,
        propsf=0.25,
        threshold=1,
        waittime=0.04,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            prophfc=prophfc,
            prophfe=prophfe,
            propsc=propsc,
            propsf=propsf,
            threshold=threshold,
            waittime=waittime,
            )
        return ugen
