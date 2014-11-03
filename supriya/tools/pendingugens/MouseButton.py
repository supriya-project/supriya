# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class MouseButton(UGen):

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
        lag=0.2,
        maxval=1,
        minval=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            lag=lag,
            maxval=maxval,
            minval=minval,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        lag=0.2,
        maxval=1,
        minval=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag=lag,
            maxval=maxval,
            minval=minval,
            )
        return ugen
