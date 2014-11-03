# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PulseDivider(UGen):

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
        div=2,
        start=0,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            div=div,
            start=start,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        div=2,
        start=0,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            div=div,
            start=start,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        div=2,
        start=0,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            div=div,
            start=start,
            trigger=trigger,
            )
        return ugen
