# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class MostChange(UGen):

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
        a=0,
        b=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a=0,
        b=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        a=0,
        b=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a=a,
            b=b,
            )
        return ugen
