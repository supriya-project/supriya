# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Ball(UGen):

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
        friction=0.01,
        g=1,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damp=damp,
            friction=friction,
            g=g,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damp=0,
        friction=0.01,
        g=1,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damp=damp,
            friction=friction,
            g=g,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        damp=0,
        friction=0.01,
        g=1,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damp=damp,
            friction=friction,
            g=g,
            source=source,
            )
        return ugen
