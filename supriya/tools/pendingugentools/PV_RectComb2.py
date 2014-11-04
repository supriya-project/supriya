# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.PV_ChainUGen import PV_ChainUGen


class PV_RectComb2(PV_ChainUGen):

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
        buffer_a=None,
        buffer_b=None,
        num_teeth=0,
        phase=0,
        width=0.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            num_teeth=num_teeth,
            phase=phase,
            width=width,
            )
        return ugen
