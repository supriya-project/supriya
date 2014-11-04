# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class SOS(Filter):

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
        a_0=0,
        a_1=0,
        a_2=0,
        b_1=0,
        b_2=0,
        source=0,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            a_2=a_2,
            b_1=b_1,
            b_2=b_2,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a_0=0,
        a_1=0,
        a_2=0,
        b_1=0,
        b_2=0,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            a_2=a_2,
            b_1=b_1,
            b_2=b_2,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        a_0=0,
        a_1=0,
        a_2=0,
        b_1=0,
        b_2=0,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            a_2=a_2,
            b_1=b_1,
            b_2=b_2,
            source=source,
            )
        return ugen
