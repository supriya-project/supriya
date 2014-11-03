# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.PV_ChainUGen import PV_ChainUGen


class PV_PhaseShift(PV_ChainUGen):

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
        integrate=0,
        shift=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            integrate=integrate,
            shift=shift,
            )
        return ugen
