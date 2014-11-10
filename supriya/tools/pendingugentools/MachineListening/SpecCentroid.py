# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SpecCentroid(UGen):

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
        buffer=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer=buffer,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        buffer=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            )
        return ugen
