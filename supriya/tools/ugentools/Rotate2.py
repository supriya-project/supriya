# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Rotate2(MultiOutUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'x',
        'y',
        'position',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        position=0,
        x=None,
        y=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=2,
            position=position,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        position=0,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            position=position,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        position=0,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            position=position,
            x=x,
            y=y,
            )
        return ugen