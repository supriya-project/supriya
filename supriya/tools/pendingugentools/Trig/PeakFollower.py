# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PeakFollower(UGen):

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
        decay=0.999,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decay=decay,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay=0.999,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay=decay,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decay=0.999,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decay=decay,
            source=source,
            )
        return ugen
