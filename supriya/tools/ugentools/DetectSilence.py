# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class DetectSilence(Filter):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'amp',
        'time',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        amp=0.0001,
        done_action=0,
        source=0,
        time=0.1,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            amp=amp,
            done_action=done_action,
            source=source,
            time=time,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        amp=0.0001,
        done_action=0,
        source=0,
        time=0.1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            done_action=done_action,
            source=source,
            time=time,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        amp=0.0001,
        done_action=0,
        source=0,
        time=0.1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            amp=amp,
            done_action=done_action,
            source=source,
            time=time,
            )
        return ugen