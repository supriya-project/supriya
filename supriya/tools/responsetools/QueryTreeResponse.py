# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.ServerResponse import ServerResponse


class QueryTreeResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_child_count',
        '_items',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        child_count=None,
        items=None,
        ):
        self._child_count = child_count
        self._items = items
        self._node_id = node_id

    ### PUBLIC PROPERTIES ###

    @property
    def child_count(self):
        return self._child_count

    @property
    def items(self):
        return self._items

    @property
    def node_id(self):
        return self._node_id
