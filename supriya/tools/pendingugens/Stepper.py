# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Stepper(UGen):

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
        max=7,
        min=0,
        reset=0,
        resetval=None,
        step=1,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            max=max,
            min=min,
            reset=reset,
            resetval=resetval,
            step=step,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        max=7,
        min=0,
        reset=0,
        resetval=None,
        step=1,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            max=max,
            min=min,
            reset=reset,
            resetval=resetval,
            step=step,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        max=7,
        min=0,
        reset=0,
        resetval=None,
        step=1,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            max=max,
            min=min,
            reset=reset,
            resetval=resetval,
            step=step,
            trigger=trigger,
            )
        return ugen
