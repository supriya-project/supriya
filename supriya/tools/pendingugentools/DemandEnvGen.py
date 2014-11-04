# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class DemandEnvGen(UGen):

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
        curve=0,
        done_action=0,
        duration=None,
        gate=1,
        level=None,
        level_bias=0,
        level_scale=1,
        reset=1,
        shape=1,
        time_scale=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            curve=curve,
            done_action=done_action,
            duration=duration,
            gate=gate,
            level=level,
            level_bias=level_bias,
            level_scale=level_scale,
            reset=reset,
            shape=shape,
            time_scale=time_scale,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        curve=0,
        done_action=0,
        duration=None,
        gate=1,
        level=None,
        level_bias=0,
        level_scale=1,
        reset=1,
        shape=1,
        time_scale=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curve=curve,
            done_action=done_action,
            duration=duration,
            gate=gate,
            level=level,
            level_bias=level_bias,
            level_scale=level_scale,
            reset=reset,
            shape=shape,
            time_scale=time_scale,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        curve=0,
        done_action=0,
        duration=None,
        gate=1,
        level=None,
        level_bias=0,
        level_scale=1,
        reset=1,
        shape=1,
        time_scale=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curve=curve,
            done_action=done_action,
            duration=duration,
            gate=gate,
            level=level,
            level_bias=level_bias,
            level_scale=level_scale,
            reset=reset,
            shape=shape,
            time_scale=time_scale,
            )
        return ugen
