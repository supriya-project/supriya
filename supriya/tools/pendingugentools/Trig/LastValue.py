# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LastValue(UGen):

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
        diff=0.01,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        diff=0.01,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        diff=0.01,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )
        return ugen
