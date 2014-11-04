# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Ringz(Filter):

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
        decaytime=1,
        frequency=440,
        source=0,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            decaytime=decaytime,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decaytime=1,
        frequency=440,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decaytime=decaytime,
            frequency=frequency,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decaytime=1,
        frequency=440,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            decaytime=decaytime,
            frequency=frequency,
            source=source,
            )
        return ugen
