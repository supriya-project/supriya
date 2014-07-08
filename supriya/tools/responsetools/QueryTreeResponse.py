# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class QueryTreeResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_query_tree_group',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        query_tree_group=None,
        osc_message=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._query_tree_group = query_tree_group
    
    ### SPECIAL METHODS ###

    def __str__(self):
        return str(self._query_tree_group)

    ### PUBLIC PROPERTIES ###

    @property
    def query_tree_group(self):
        return self._query_tree_group