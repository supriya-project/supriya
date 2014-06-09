# -*- encoding: utf-8 -*-
from supriya.tools.responselib.ServerResponse import ServerResponse


class TriggerResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id',
        '_trigger_id',
        '_trigger_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        trigger_id=None,
        trigger_value=None,
        ):
        self._node_id = node_id
        self._trigger_id = trigger_id
        self._trigger_value = trigger_value

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def trigger_id(self):
        return self._trigger_id

    @property
    def trigger_value(self):
        return self._trigger_value
