# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FreeVerb(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_argument_names = (
        'source',
        'mix',
        'room_size',
        'damping',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0.5,
        mix=0.33,
        room_size=0.5,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            mix=mix,
            room_size=room_size,
            source=source,
            )
