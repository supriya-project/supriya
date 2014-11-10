# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InRect(UGen):

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
        rect=None,
        x=0,
        y=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            rect=rect,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        rect=None,
        x=0,
        y=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rect=rect,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        rect=None,
        x=0,
        y=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rect=rect,
            x=x,
            y=y,
            )
        return ugen
