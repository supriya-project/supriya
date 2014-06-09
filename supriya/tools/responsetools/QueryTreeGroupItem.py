# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class QueryTreeGroupItem(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_child_count',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        child_count=None,
        ):
        self._child_count = child_count
        self._node_id = node_id

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def child_count(self):
        return self._child_count
