# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ModDif(UGen):

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
        mod=1,
        x=0,
        y=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            mod=mod,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        mod=1,
        x=0,
        y=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            mod=mod,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        mod=1,
        x=0,
        y=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            mod=mod,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        mod=1,
        x=0,
        y=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            mod=mod,
            x=x,
            y=y,
            )
        return ugen
