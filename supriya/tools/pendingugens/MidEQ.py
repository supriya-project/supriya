# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class MidEQ(Filter):

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
        db=0,
        frequency=440,
        reciprocal_of_q=1,
        source=0,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        db=0,
        frequency=440,
        reciprocal_of_q=1,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        db=0,
        frequency=440,
        reciprocal_of_q=1,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen
