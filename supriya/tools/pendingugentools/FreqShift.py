# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FreqShift(UGen):

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
        frequency=0,
        phase=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=0,
        phase=0,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            source=source,
            )
        return ugen
