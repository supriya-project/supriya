# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LinXFade2(UGen):

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
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        in_a=None,
        in_b=0,
        level=1,
        pan=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            in_a=in_a,
            in_b=in_b,
            level=level,
            pan=pan,
            )
        return ugen
