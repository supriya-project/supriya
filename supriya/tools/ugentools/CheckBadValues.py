# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class CheckBadValues(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'ugen_id',
        'post_mode',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ugen_id=0,
        post_mode=2,
        source=None,
        ):
        assert int(post_mode) in (0, 1, 2)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        ugen_id=0,
        post_mode=2,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        ugen_id=0,
        post_mode=2,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
            )
        return ugen