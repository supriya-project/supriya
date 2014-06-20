# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PauseSelf(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return source
