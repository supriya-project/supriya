# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Rotate2(MultiOutUGen):

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
        pos=0,
        x=None,
        y=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            pos=pos,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        pos=0,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pos=pos,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        pos=0,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            pos=pos,
            x=x,
            y=y,
            )
        return ugen
