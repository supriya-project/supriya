# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.PV_ChainUGen import PV_ChainUGen


class PV_ConformalMap(PV_ChainUGen):

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
        aimag=0,
        areal=0,
        buffer=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            aimag=aimag,
            areal=areal,
            buffer=buffer,
            )
        return ugen
