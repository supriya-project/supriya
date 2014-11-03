# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Normalizer(UGen):

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
        duration=0.01,
        level=1,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            duration=duration,
            level=level,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        duration=0.01,
        level=1,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            duration=duration,
            level=level,
            source=source,
            )
        return ugen
