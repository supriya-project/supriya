# -*- encoding: utf-8 -*-
from supriya.tools.responselib.ServerResponse import ServerResponse


class NodeInfoResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_head_node_id',
        '_is_group',
        '_message_head',
        '_next_node_id',
        '_node_id',
        '_parent_group_id',
        '_previous_node_id',
        '_tail_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        message_head=None,
        node_id=None,
        parent_group_id=None,
        previous_node_id=None,
        next_node_id=None,
        is_group=None,
        head_node_id=None,
        tail_node_id=None,
        ):
        self._head_node_id = head_node_id
        self._is_group = is_group
        self._message_head = message_head
        self._next_node_id = next_node_id
        self._node_id = node_id
        self._parent_group_id = parent_group_id
        self._previous_node_id = previous_node_id
        self._tail_node_id = tail_node_id

    ### PUBLIC PROPERTIES ###

    @property
    def head_node_id(self):
        return self._head_node_id

    @property
    def is_group(self):
        return self._is_group

    @property
    def message_head(self):
        return self._message_head

    @property
    def next_node_id(self):
        return self._next_node_id

    @property
    def node_id(self):
        return self._node_id

    @property
    def parent_group_id(self):
        return self._parent_group_id

    @property
    def previous_node_id(self):
        return self._previous_node_id

    @property
    def tail_node_id(self):
        return self._tail_node_id
