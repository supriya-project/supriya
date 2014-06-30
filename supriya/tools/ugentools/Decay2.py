# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Decay2(Filter):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'attack_time',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attack_time=None,
        decay_time=None,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=None,
        decay_time=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        attack_time=None,
        decay_time=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen
