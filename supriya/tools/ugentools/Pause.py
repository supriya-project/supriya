# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Pause(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = (
        'gate',
        'node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        gate=None,
        node_id=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            gate=gate,
            node_id=node_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        gate=None,
        node_id=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            gate=gate,
            node_id=node_id,
            )
        return ugen