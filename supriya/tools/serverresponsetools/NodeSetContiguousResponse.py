# -*- encoding: utf-8 -*-
from supriya.tools.serverresponsetools.ServerResponse import ServerResponse


class NodeSetContiguousResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        items=None,
        ):
        self._items = items
        self._node_id = node_id

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def node_id(self):
        return self._node_id
