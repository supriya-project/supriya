# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class MoogFF(Filter):

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
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )
        return ugen
