# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.DUGen import DUGen


class Dpoll(DUGen):

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
        label=None,
        run=1,
        source=None,
        trigid=-1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            run=run,
            source=source,
            trigid=trigid,
            )
        return ugen

    # def new1(): ...
