# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Spring(UGen):

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
        damp=0,
        source=0,
        spring=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damp=damp,
            source=source,
            spring=spring,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damp=0,
        source=0,
        spring=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damp=damp,
            source=source,
            spring=spring,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        damp=0,
        source=0,
        spring=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damp=damp,
            source=source,
            spring=spring,
            )
        return ugen
