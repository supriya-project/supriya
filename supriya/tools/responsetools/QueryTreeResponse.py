# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class QueryTreeResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id',
        '_query_tree_group',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        osc_message=None,
        query_tree_group=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._node_id = node_id
        self._query_tree_group = query_tree_group
    
    ### SPECIAL METHODS ###

    def __str__(self):
        return str(self._query_tree_group)

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def query_tree_group(self):
        return self._query_tree_group
