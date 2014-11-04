# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Control import Control


class LagControl(Control):

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
        ):
        Control.__init__(
            self,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        lags=None,
        values=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lags=lags,
            values=values,
            )
        return ugen
