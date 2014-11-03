# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.PV_ChainUGen import PV_ChainUGen


class PV_RandComb(PV_ChainUGen):

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
        buffer=None,
        trigger=0,
        wipe=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen
