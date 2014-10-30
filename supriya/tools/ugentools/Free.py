# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Free(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        trigger=None,
        node_id=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            trigger=trigger,
            node_id=node_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        trigger=None,
        node_id=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            trigger=trigger,
            node_id=node_id,
            )
        return ugen