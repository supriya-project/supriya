# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.AmpComp import AmpComp


class AmpCompA(AmpComp):

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
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        AmpComp.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )
        return ugen
