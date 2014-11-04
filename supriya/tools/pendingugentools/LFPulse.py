# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class LFPulse(PureUGen):

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
        frequency=440,
        iphase=0,
        width=0.5,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            iphase=iphase,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        iphase=0,
        width=0.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            iphase=iphase,
            width=width,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        iphase=0,
        width=0.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            iphase=iphase,
            width=width,
            )
        return ugen
