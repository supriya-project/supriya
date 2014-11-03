# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.PV_ChainUGen import PV_ChainUGen


class FFT(PV_ChainUGen):

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
        active=1,
        buffer=None,
        hop=0.5,
        source=0,
        winsize=0,
        wintype=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            active=active,
            buffer=buffer,
            hop=hop,
            source=source,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen
