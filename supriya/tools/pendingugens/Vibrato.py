# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Vibrato(PureUGen):

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
        delay=0,
        depth=0.02,
        depth_variation=0.1,
        frequency=440,
        iphase=0,
        onset=0,
        rate=6,
        rate_variation=0.04,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            delay=delay,
            depth=depth,
            depth_variation=depth_variation,
            frequency=frequency,
            iphase=iphase,
            onset=onset,
            rate=rate,
            rate_variation=rate_variation,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        delay=0,
        depth=0.02,
        depth_variation=0.1,
        frequency=440,
        iphase=0,
        onset=0,
        rate=6,
        rate_variation=0.04,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            delay=delay,
            depth=depth,
            depth_variation=depth_variation,
            frequency=frequency,
            iphase=iphase,
            onset=onset,
            rate=rate,
            rate_variation=rate_variation,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        delay=0,
        depth=0.02,
        depth_variation=0.1,
        frequency=440,
        iphase=0,
        onset=0,
        rate=6,
        rate_variation=0.04,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            delay=delay,
            depth=depth,
            depth_variation=depth_variation,
            frequency=frequency,
            iphase=iphase,
            onset=onset,
            rate=rate,
            rate_variation=rate_variation,
            )
        return ugen
