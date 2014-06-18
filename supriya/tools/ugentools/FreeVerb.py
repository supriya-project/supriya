# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.synthdeftools.UGen import UGen


class FreeVerb(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        Argument('mix'),
        Argument('room_size'),
        Argument('damping'),
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
