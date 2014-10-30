# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pan2(MultiOutUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'position',
        'level',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        level=1.,
        position=0.,
        rate=None,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            channel_count=2,
            level=level,
            position=position,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1.,
        position=0.,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            position=position,
            level=level,
            )
        return ugen